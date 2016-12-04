var search = document.getElementById("document-search");

// var cars = ["Calculus 1 For Engineers Exam 1",
//             "Calculus 2 For Engineers Exam 3",
//             "Discrete Math for Computer Scientists Final Exam",
//             "Biology Laboratory for Biology Majors Quiz 5"];

new autoComplete({
    selector: search,
    minChars: 2,
    source: function(term, response) {

        axios.get('/search?term=' + term)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });

    }
});

function popModal(modalType)
{
    var search_container = document.getElementById("search-container");
    var correct_modal = document.getElementById(modalType + "-modal");
    var login_modal = document.getElementById("login-modal");
    var register_modal = document.getElementById("register-modal");
    var login_btn = document.getElementById("login-btn");
    var register_btn = document.getElementById("register-btn");
    var back_btn = document.getElementById("back-btn");

    if(back_btn.style.display === "none")
    {
        search_container.style.display = "none";
        correct_modal.style.display = "block";
        login_btn.style.display = "none";
        register_btn.style.display = "none";
        back_btn.style.display = "block";
    }
    else if(back_btn.style.display === "block")
    {
        search_container.style.display = "block";
        login_modal.style.display = "none";
        register_modal.style.display = "none";
        login_btn.style.display = "block";
        register_btn.style.display = "block";
        back_btn.style.display = "none";
    }



}
