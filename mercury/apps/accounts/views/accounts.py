from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Membership, Site
from apps.accounts.serializers import MembershipSerializer, SiteSerializer
from apps.accounts.tasks import task_init_site
from apps.accounts.views.utils import HasEditRights, get_slug


class SiteViewSet(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Site.objects.filter(
            Q(hosts__user=self.request.user, hosts__rights=Membership.EDIT)
            | Q(created_by=self.request.user)
        )

    def create(self, request, *args, **kwargs):
        # here we can check number of allowed sites
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        try:
            # create a database instance
            with transaction.atomic():
                instance = serializer.save(created_by=self.request.user)

                instance.slug = get_slug(instance.slug, instance.title)

                instance.save()
        except Exception as e:
            raise APIException(str(e))

    def perform_update(self, serializer):
        updated_instance = serializer.save()
        # lets check slug if we update it
        new_slug = self.request.data.get("slug")
        if new_slug is not None:
            updated_instance.slug = get_slug(new_slug, updated_instance.title)
            updated_instance.save()

    def destroy(self, request, *args, **kwargs):
        """Only owner can delete object"""
        try:
            instance = self.get_object()
            if instance.created_by == self.request.user:
                self.perform_destroy(instance)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated, HasEditRights]

    def get_queryset(self):
        return Membership.objects.filter(host__id=self.kwargs["site_id"])

    def perform_create(self, serializer):
        try:
            # create a database instance
            with transaction.atomic():
                site = Site.objects.get(pk=self.kwargs.get("site_id"))
                user = User.objects.get(pk=self.request.data.get("user_id"))
                instance = serializer.save(
                    host=site, user=user, created_by=self.request.user
                )
                instance.save()
        except Exception as e:
            raise APIException(str(e))


class GetSiteView(APIView):
    def get(self, request, site_slug, format=None):
        sites = Site.objects.filter(slug=site_slug)
        if not sites:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if sites[0].share == Site.PUBLIC:
            return Response(SiteSerializer(sites[0]).data)

        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)

        sites = sites.filter(
            # any Membership (VIEW or EDIT) or owner
            Q(hosts__user=self.request.user)
            | Q(created_by=self.request.user)
        )

        if not sites:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(SiteSerializer(sites[0]).data)


class InitializeSite(APIView):
    permission_classes = [permissions.IsAuthenticated, HasEditRights]

    def post(self, request, site_id, format=None):
        try:
            with transaction.atomic():
                job_params = {"site_id": site_id}
                transaction.on_commit(lambda: task_init_site.delay(job_params))
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(str(e))
