/**
 * Adds a notification error if the error response has 404 status code.
 */
export function notify404(dispatch, error, title, message) {
  if (error.response && error.response.status === 404) {
    dispatch(
      'notification/error',
      {
        title: title,
        message: message
      },
      { root: true }
    )
  }
}

/**
 * Adds a notification error if the response error is equal to the provided
 * error code.
 */
export function notifyError(dispatch, error, error_code, title, message) {
  if (error.responseError === error_code) {
    dispatch(
      'notification/error',
      {
        title: title,
        message: message
      },
      { root: true }
    )
  }
}
