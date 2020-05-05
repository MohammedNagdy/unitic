
// function to check the field secondary account to do some ajax
// and show and hide some fields for better ui
function checkAccountName(){
  var account = $('#id_secondary_account option:selected').text();
  var percentage = document.getElementById('id_percentage');
  var recursion = document.getElementById('id_recursion');
  var dateOfPayment = document.getElementById('id_date_of_payment');
  var dateOfService = document.getElementById('id_date_of_service');
  if (account === "قروض"){
    percentage.style.display = "block";
    recursion.style.display = 'block';
    dateOfPayment.style.display = 'block';
    }
  else if ( account === "مرتبات الموظفين"){
    recursion.style.display = 'block';
  }
  else if ( account === "المبيعات"){
    dateOfService.style.display = 'block';
  }
  else {
      percentage.style.display = "none";
      recursion.style.display = 'none';
      dateOfPayment.style.display = 'none';
      dateOfService.style.display = 'none';
    }
 }

checkAccountName();

// add the even listener to see what account in the secondary account field
var accountName = document.getElementById('id_secondary_account');
accountName.addEventListener('change', () => {
  var account = $('#id_secondary_account option:selected').text();
  var percentage = document.getElementById('id_percentage');
  var recursion = document.getElementById('id_recursion');
  var dateOfPayment = document.getElementById('id_date_of_payment');
  var dateOfService = document.getElementById('id_date_of_service');
  if (account === "قروض"){
    percentage.style.display = "block";
    recursion.style.display = 'block';
    dateOfPayment.style.display = 'block';
    }
  else if ( account === "مرتبات الموظفين"){
    recursion.style.display = 'block';
  }
  else if ( account === "المبيعات"){
    dateOfService.style.display = 'block';
  }
  else {
      percentage.style.display = "none";
      recursion.style.display = 'none';
      dateOfPayment.style.display = 'none';
      dateOfService.style.display = 'none';
    }
 })
