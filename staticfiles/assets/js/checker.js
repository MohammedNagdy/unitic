//this file for password checking while registering

password1.addEventListener('change', () =>{
  const password1 = document.querySelector('#id_password1').value;
  const password2 = document.querySelector('#id_password2').value;
  let strength = document.getElementById('pass-strength');
  console.log(password1)

    if (password2.length > 8 ){
      strength.innerHTML = "strong";
      strength.classList.remove('text-danger');
      strength.classList.add('text-success')
    }

  }
);
