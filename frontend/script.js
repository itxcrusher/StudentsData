console.clear();

// AWS SDK Configuration
AWS.config.update({ region: "us-east-1" });
//"https://n2wp9qmj5i.execute-api.us-east-1.amazonaws.com/Prod/students"
var API_URL = 
  "https://kkwrv5ek42.execute-api.us-east-1.amazonaws.com/Dev/items";

// Get all items
function fetchData(params) {
  $.ajax({
    url: API_URL,
    method: "GET",
    dataType: "json",
    success: function (responseData) {
      var array = responseData;
      var tableBody = document.getElementById('tableBody');
      tableBody.innerHTML = '';
      array.forEach(function(obj) {
        var row = tableBody.insertRow();
        var cell = row.insertCell(0);
        cell.textContent = obj.id;
      });
    },
    error: function (error) {
      console.error("AJAX error:", error);
    },
  });
}
fetchData();

// Get item by ID
$("#getForm").submit((e) => {
  e.preventDefault();
  var itemId = $("#getForm #get-id").val();
  $.ajax({
    url: API_URL + "/" + itemId,
    method: "GET",
    dataType: "json",
    success: function (responseData) {
      $("#display-id").html(JSON.stringify(responseData, null, 2));
    },
    error: function (error) {
      alert("Unsuccessful!");
    },
  });
});

// Put Items
$("#putForm").submit((e) => {
  e.preventDefault();
  var formData = {
    id: $("#putForm #put-id").val(),
  };
  $.ajax({
    url: API_URL,
    method: "POST",
    dataType: "json",
    contentType: "application/json",
    data: JSON.stringify(formData),
    success: function (responseData) {
      fetchData();
    },
    error: function (error) {
      console.error("AJAX error:", error);
      alert("Error creating item.");
    },
  });
});

// Update Items
$("#updateForm").submit((e) => {
  e.preventDefault();
  var itemId = $("#updateForm #update-id").val();
  var formData = {
    id: $("#updateForm #new-id").val(),
  };
  $.ajax({
    url: API_URL + "/" + itemId,
    method: "PATCH",
    dataType: "json",
    contentType: "application/json",
    data: JSON.stringify(formData),
    success: function (responseData) {
      fetchData();
    },
    error: function (error) {
      console.error("AJAX error:", error);
      alert("Error updating item.");
    },
  });
});

// Delete Item by Id
$("#deleteForm").submit((e) => {
  e.preventDefault();
  var itemId = $("#deleteForm #delete-id").val();
  $.ajax({
    url: API_URL + "/" + itemId,
    method: "DELETE",
    dataType: "json",
    success: function (responseData) {
      fetchData();
    },
    error: function (error) {
      console.error("AJAX error:", error);
      alert("Error deleting item!");
    },
  });
});