$(document).ready(function() {
    // Intercept the form submission
    $("#clubAdviceForm").submit(function(event) {
      event.preventDefault(); // Prevent the form from submitting normally
      
      // Get the form data
      var formData = $(this).serialize();
  
      // Send an AJAX POST request
      $.ajax({
        type: "POST",
        url: "/getClubAdviceprocess",
        data: formData,
        success: function(response) {
          // Clear the previous content in the output space
          //$("#output_space").empty();
          
          // Add the new club advice content
          response.output.forEach(function(line) {
            $("#output_space").append("<p>" + line + "</p>");
          });
        },
        error: function(error) {
          console.log(error);
        }
      });
    });
  
    // Reset button
    $("#clear").click(function() {
      $("#output_space").empty(); // Clear the output space
      $("#clubAdviceForm")[0].reset(); // Reset the form
    });
  });



  