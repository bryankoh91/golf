function myFunction1() {
    var x = document.getElementById("selected_data_type1").value;
    //alert(x)
    document.getElementById("email").value = x;

    getClub(x);
} //end of myFunction

function myFunction2() {
    var x = document.getElementById("selected_data_type2").value;
    //alert(x)
    document.getElementById("club").value = x;


} //end of myFunction

function getClub(email) {
    $.ajax({
        url: "/getClubs",
        type: "POST",
        data: {
            email: email
        },
        error: function() {
            alert("Error");
        }, //end of error
        success: function(data, status, xhr) {
            var club_list = [];

            for (var clubLabel of data.myClubs) {
                club_list.push(clubLabel);
            }

            populate("#selected_data_type2", club_list)

        } //end of sucess
    }); //end of ajax call
} //end of getClub


function populate(selector, club_list) {

    $(selector).empty();
    $(selector).append("<option value=\"all\">Select One Club (by label)</option>");

    if (club_list.length != 0) {
        for (var i=0; i<club_list.length; i++) {
            let select_str = "<option value=\"" + club_list[i] + "\">" + club_list[i] + "</option>";
            $(selector).append(select_str);
        }
    }
} //end of populate

function getClubHeight() {
    var email = document.getElementById("selected_data_type1").value;
    var label = document.getElementById("selected_data_type2").value;
    //alert(x);
    
    $.ajax({
        url:"/getClubHeight",
        type: "POST",
        data: {
            email: email,
            label: label
        },
        error: function() {
            alert("Error");
        }, //end of error
        success: function(data, status, xhr) {
            document.getElementById("club_height").innerHTML = "The height of club " + label +" is " + data.ClubHeight + "mm";
        } //end of success
    }) //end of ajax call
} //getClubHeight