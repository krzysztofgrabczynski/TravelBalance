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
  if (password.length < 8)
    return false

  if (!containsSpecialCharacter(password))
    return false

  if (!containsUpperLetter(password))
    return false

  if (!containsNumber(password))
    return false

  if (!passwordsMatch(password, passwordRepeated))
    return false

  return true
}
