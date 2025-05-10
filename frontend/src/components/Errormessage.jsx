function ErrorMessage({ error }) {
  return error ? <div className="error-message">{error}</div> : null;
}

export default ErrorMessage;