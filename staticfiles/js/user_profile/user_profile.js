/**
 * Created by Jhon Edison Gomez on 6/01/2018.
 */
     $(document).ready(function(){
      $('.parallax').parallax();
    });

   $(document).ready(function(){
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
  });
       

$(".button-collapse").sideNav();
  var $input = $('.datepicker').pickadate({
    // Strings and translations
    monthsFull: ['Enero', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Hoy',
    clear: 'Limpiar',
    close: 'Ok',
    format: 'dd/mm/yyyy',
    formatSubmit: 'dd/mm/yyyy',
    closeOnSelect: true // Close upon selecting a date,
  });

var Users = {

    signIn: function(){

        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;

        if(email != "" || password != ""){

             $.ajax({
                 type: 'get',
                 data:{'username':email, 'password':password},
                 url:'/usuario/iniciar-sesion/',
                 success: function (response) {
                     var message = response.message;
                     var isError = response.isError;
                     var authenticated = response.authenticated;

                     if(!isError){
                        if(authenticated){
                            location.reload();
                        }else{
                            Materialize.toast(message, 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
                        }
                     }else{
                        Materialize.toast(message, 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
                     }
                 }

             });


        }else{
            Materialize.toast('Los datos en el formulario no son validos o estan vacios', 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
        }
    },

    openSignUpForm: function(){

        signUpForm.reset();

        $('#modal1').modal('open');
    },

    signUpForm: function(){

        var firstname = document.getElementById("firstnameReg").value;
        var lastname = document.getElementById("lastnameReg").value;
        var email = document.getElementById("emailReg").value;
        var password = document.getElementById("passwordReg").value;
        var passwordAgain = document.getElementById("passwordAgain").value;

        if(firstname != "" || lastname != "" || email != ""
            || password != "" || passwordAgain != ""){




        }else{

            Materialize.toast('Los datos en el formulario no son validos o estan vacios', 3000, 'rounded')
        }

    },

}

