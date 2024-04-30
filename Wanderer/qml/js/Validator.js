// validator.js
function validateUsername(username) {
  var regex = /^[a-zA-Z0-9._-]{1,}$/
  return regex.test(username)
}

function validateEmail(email) {
  var regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  return regex.test(email)
}

function containsSpecialCharacter(text) {
  var specialCharacters = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/
  return specialCharacters.test(text)
}

function containsNumber(text) {
  var numberPattern = /[0-9]+/
  return numberPattern.test(text)
}

function containsUpperLetter(text) {
  var upperLetter = /[A-Z]/
  return upperLetter.test(text)
}

function passwordsMatch(password, passwordRepeated) {
  return password === passwordRepeated && password.length !== 0
}

function validatePassword(password, passwordRepeated) {
  var isValid = true

  if (password.length < 8) {
    isValid = false
  }

  if (!containsSpecialCharacter(password)) {
    isValid = false
  }

  if (!containsUpperLetter(password)) {
    isValid = false
  }

  if (!containsNumber(password)) {
    isValid = false
  }

  if (!passwordsMatch(password, passwordRepeated)) {
    isValid = false
  }

  return isValid
}
