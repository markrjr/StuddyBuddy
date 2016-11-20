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

function popModal()
{
    var login_btn = document.getElementById("login-btn");
    var auth_modal = document.getElementById("auth-modal");
    var search_container = document.getElementById("search-container");

    if(auth_modal.style.display == "none")
    {
        search_container.style.display = "none";
        auth_modal.style.display = "block";
        login_btn.innerText = "Back";
    }
    else if(auth_modal.style.display == "block")
    {
        auth_modal.style.display = "none";
        search_container.style.display = "block";
        login_btn.innerText = "Login";
    }
}
