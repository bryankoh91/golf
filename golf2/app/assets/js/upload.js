function myFunction8() {
    var x = document.getElementById("selected_golfer").value;
    document.getElementsByClassName("chosen_email")[0].value = x; // Use [0] to access the first element in the collection
    getUser(x);
}
