import React, { useRef, useState } from 'react';
import classes from '../styles';
import { useNavigate } from 'react-router-dom';
import AuthService from '../services/auth.service';

const Register = () => {
    const navigate = useNavigate();
    const handleFormSubmit = (e) => {
        e.preventDefault();
    };
    const emailRef = useRef();
    const passwordRef = useRef();
    const passwordRepeatRef = useRef();
    const [errorMessage, setErrorMessage] = useState('');

    const login = () => {
        navigate("/");
    }
    const register = (e) => {
        let email = emailRef.current.value;
        let password = passwordRef.current.value;
        let passwordRepeat = passwordRepeatRef.current.value;

        if (email === "") {
            setErrorMessage("Please Input Email.");
            return;
        }
        if (password === "" || passwordRepeat === "") {
            setErrorMessage("Please Input Password.");
            return;
        }
        setErrorMessage("");

        AuthService.register(email, password, passwordRepeat)
            .then(() => {
                navigate("/dashboard");
            })
            .catch((error) => {
                if (error.response) {
                    setErrorMessage(error.response.data.detail);
                } else {
                    setErrorMessage("Something went wrong.");
                }
            });
    }

    return (
        <div className={classes.container}>
            <div className={classes.formContainer}>
                <h1 className={classes.formHeading}>Register your account</h1>

                <form onSubmit={handleFormSubmit}>
                    <div className={classes.formInput}>
                        <label htmlFor='email' className={classes.label}>Email</label>
                        <input
                            type='email'
                            ref={emailRef}
                            placeholder='Your Email'
                            className={classes.input}
                        />
                    </div>
                    <div className={classes.formInput}>
                        <label htmlFor='password' className={classes.label}>Password</label>
                        <input
                            type='password'
                            ref={passwordRef}
                            placeholder='Your Password'
                            className={classes.input}
                        />
                    </div>
                    <div className={classes.formInput}>
                        <label htmlFor='password' className={classes.label}>Retype</label>
                        <input
                            type='password'
                            ref={passwordRepeatRef}
                            placeholder='Confirm Password'
                            className={classes.input}
                        />
                    </div>
                    <div class={classes.errorMessage}>
                        {errorMessage}
                    </div>
                    <div className={classes.btnContainer}>
                        <button className={classes.btn} onClick={e => register(e)}>Register</button>
                    </div>
                    <div className={classes.text}>
                        Or
                    </div>
                    <div className={classes.btnContainer}>
                        <button className={classes.btn} onClick={() => login()}>Login</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Register;
