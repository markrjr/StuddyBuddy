var blah = document.getElementById("document-search");

var cars = ["Calculus 1 For Engineers Exam 1",
            "Calculus 2 For Engineers Exam 3",
            "Discrete Math for Computer Scientists Final Exam",
            "Biology Laboratory for Biology Majors Quiz 5"];

new autoComplete({
    selector: blah,
    minChars: 2,
    source: function(term, suggest){
        term = term.toLowerCase();
        var choices = cars;
        var matches = [];
        for (i=0; i<choices.length; i++)
            if (~choices[i].toLowerCase().indexOf(term))
            {
              matches.push(choices[i]);
            }
        suggest(matches);
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
