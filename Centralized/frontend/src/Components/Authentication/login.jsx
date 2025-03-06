import React, { useState } from "react";
import { Form, Button, Container } from "react-bootstrap";
import UseLogin from "../../Hooks/useLogin";

function Login() {
    const [loginData, setLoginData] = useState({
        ldap: "",
        password: ""
    });

    const { Login } = UseLogin();

    const handleChange = (e) => {
        setLoginData({
            ...loginData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        Login(loginData);
    };

    return (
        <Container className="my-5 w-50 bg-secondary border border-dark rounded py-4 px-4">
            <h2 className="text-center mb-4">LOGIN</h2>
            <Form>

                {/* LDAP Email */}
                <Form.Group className="mb-3" controlId="ldap">
                    <Form.Label className="text-white fs-5">LDAP Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Enter your LDAP email"
                        name="ldap"
                        autoComplete="LDAP Email"
                        value={loginData.ldap}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                {/* Password */}
                <Form.Group className="mb-3" controlId="password">
                    <Form.Label className="text-white fs-5">Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Enter password"
                        name="password"
                        autoComplete="current-password"
                        value={loginData.password}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                <div className="d-flex justify-content-center">
                    <Button variant="primary" type="submit" className="w-25 fs-5" onClick={handleSubmit}>
                        Login
                    </Button>
                </div>


            </Form>
        </Container>
    )
}

export default Login;

