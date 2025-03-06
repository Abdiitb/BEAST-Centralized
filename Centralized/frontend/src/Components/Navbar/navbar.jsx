import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from "react-router-dom";
import { useContext } from 'react';
import { AuthContext } from '../../Contexts/AuthContext';

function NavBar() {
    const { loggedIn } = useContext(AuthContext);

    return (
        <Navbar bg="primary" data-bs-theme="dark">
            <Container>
                <Navbar.Brand as={Link} to="/" className='fs-2'>SARC</Navbar.Brand>
                {loggedIn ? (
                    <Nav className='fs-3 d-flex gap-5'>
                        <Nav.Link as={Link} to="/" >Home</Nav.Link>
                    </Nav>

                ) : (
                    <Nav className='fs-3 d-flex gap-5'>
                        <Nav.Link as={Link} to="/" >Home</Nav.Link>
                        <Nav.Link as={Link} to="/signup" >Signup</Nav.Link>
                        <Nav.Link as={Link} to="/login" >Login</Nav.Link>
                    </Nav>
                )}

            </Container>
        </Navbar>
    )
}

export default NavBar;