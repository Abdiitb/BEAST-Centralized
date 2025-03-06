import React, { useState } from "react";
import { Form, Button, Container } from "react-bootstrap";
import UseSignup from "../../Hooks/useSignup";

const HOSTEL_CHOICES = {
    H1: "Hostel 1",
    H2: "Hostel 2",
    H3: "Hostel 3",
    H4: "Hostel 4",
    H5: "Hostel 5",
    H6: "Hostel 6",
    H9: "Hostel 9",
    H10: "Hostel 10",
    H11: "Hostel 11",
    H12: "Hostel 12",
    H13: "Hostel 13",
    H14: "Hostel 14",
    H15: "Hostel 15",
    H16: "Hostel 16",
    H17: "Hostel 17",
    H18: "Hostel 18",
};

function Signup() {
    const [formData, setFormData] = useState({
        ldap: "",
        password: "",
        username: "",
        email: "",
        roll_number: "",
        hostel_number: "",
    });

    const { signup } = UseSignup();
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        signup(formData);
    };

    return (
        <Container className="my-4 w-50 bg-secondary border border-dark rounded py-4 px-4">
            <h2 className="text-center">SIGN UP</h2>
            <Form>

                {/* LDAP Email */}
                <Form.Group className="mb-3" controlId="ldap">
                    <Form.Label className="text-white fs-5">LDAP Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Enter your LDAP email"
                        name="ldap"
                        autoComplete="email"
                        value={formData.ldap}
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
                        autoComplete="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                {/* Username */}
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label className="text-white fs-5">Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter your username"
                        name="username"
                        autoComplete="username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                {/* Personal Email */}
                <Form.Group className="mb-3" controlId="personalEmail">
                    <Form.Label className="text-white fs-5">Personal Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Enter your personal email"
                        name="email"
                        autoComplete="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                {/* Roll Number */}
                <Form.Group className="mb-3" controlId="rollNumber">
                    <Form.Label className="text-white fs-5">Roll Number</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter your roll number"
                        name="roll_number"
                        autoComplete="roll_number"
                        value={formData.roll_number}
                        onChange={handleChange}
                        required
                    />
                </Form.Group>

                {/* Hostel Number */}
                <Form.Group className="mb-3" controlId="hostelNumber">
                    <Form.Label className="text-white fs-5">Hostel Number</Form.Label>
                    <Form.Select
                        name="hostel_number"
                        value={formData.hostel_number}
                        autoComplete="hostel_number"
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select your hostel</option>
                        {Object.entries(HOSTEL_CHOICES).map(([key, value]) => (
                            <option key={key} value={key}>
                                {value}
                            </option>
                        ))}
                    </Form.Select>
                </Form.Group>

                {/* Submit Button */}
                <div className="d-flex justify-content-center">
                    <Button variant="primary" type="submit" className="w-25 fs-5" onClick={handleSubmit}>
                        Sign Up
                    </Button>
                </div>


            </Form>
        </Container>
    );
}

export default Signup;
