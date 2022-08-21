//input
let username = document.getElementById('id_username')
let email = document.getElementById('id_email')
let password1 = document.getElementById('id_password1')
let password2 = document.getElementById('id_password2')
let name = document.getElementById('id_name')
let phone = document.getElementById('id_phone')
//help text
let usernameHelp = document.getElementById('form-help-username')
let emailHelp = document.getElementById('form-help-email')
let password1Help = document.getElementById('form-help-password1')
let password2Help = document.getElementById('form-help-password2')
let nameHelp = document.getElementById('form-help-name')
let phoneHelp = document.getElementById('form-help-phone')


usernameHelp.classList.remove("hidden")
console.log(username.classList)
console.log(usernameHelp.classList)

function show(i) {
  usernameHelp.classList.add("hidden")
  emailHelp.classList.add("hidden")
  password1Help.classList.add("hidden")
  password2Help.classList.add("hidden")
  nameHelp.classList.add("hidden")
  phoneHelp.classList.add("hidden")
  i.classList.remove("hidden")
}


username.addEventListener('focus', () => {
  show(usernameHelp)
});

email.addEventListener('focus', () => {
  show(emailHelp)
});
password1.addEventListener('focus', () => {
  show(password1Help)
});

password2.addEventListener('focus', () => {
  show(password2Help)
});
name.addEventListener('focus', () => {
  show(nameHelp)
});

phone.addEventListener('focus', () => {
  show(phoneHelp)
});
