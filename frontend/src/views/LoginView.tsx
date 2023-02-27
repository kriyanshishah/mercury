/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchToken } from "../components/authSlice";
import Footer from "../components/Footer";
import HomeNavBar from "../components/HomeNavBar";
import { getFetchingIsPro, getIsPro } from "../components/versionSlice";

import ProFeatureAlert from "../components/ProFeatureAlert";
import { useNavigate } from "react-router-dom";
import { isPublic } from "../components/Sites/sitesSlice";

export default function LoginView() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const isPro = useSelector(getIsPro);
  const fetchingIsPro = useSelector(getFetchingIsPro);
  const isSitePublic = useSelector(isPublic);

  document.body.style.backgroundColor = "#f5f5f5";

  let redirectPath = "/";
  const navigate = useNavigate();

  return (
    <div className="App">
      <HomeNavBar isSitePublic={isSitePublic} isPro={isPro} username={""} />

      {!isPro && !fetchingIsPro && (
        <ProFeatureAlert featureName={"authentication"} />
      )}
      {isPro && (
        <div className="div-signin text-center">
          <form
            className="form-signin"
            onSubmit={(e) => {
              e.preventDefault();
              e.stopPropagation();
              dispatch(fetchToken(email, password, redirectPath, navigate));
            }}
          >
            <h3 className="h3 mb-3 font-weight-normal">Please sign in</h3>
            <label className="sr-only">Email</label>
            <input
              type="email"
              id="inputEmail"
              className="form-control"
              placeholder="Email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
              }}
              required
            />
            <label className="sr-only">Password</label>
            <input
              type="password"
              id="inputPassword"
              className="form-control"
              placeholder="Password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
              }}
              required
            />
            <button
              className="btn btn-lg btn-primary btn-block"
              type="submit"
              style={{ margin: "5px" }}
              disabled={email === "" || password === ""}
            >
              <i className="fa fa-sign-in" aria-hidden="true"></i> Log in
            </button>
          </form>
          <div
            className="mx-auto"
            style={{ width: "400px", marginTop: "40px" }}
          >
            <p className="text-muted">
              No account? <br/> Please contact administrator to create account for
              you.
            </p>
          </div>
        </div>
      )}
      <Footer />
    </div>
  );
}
