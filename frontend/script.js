console.clear();

// AWS SDK Configuration
AWS.config.update({
    region: 'us-east-1',
});

// API Gateway endpoint
// const apiEndpoint = 'https://n2wp9qmj5i.execute-api.us-east-1.amazonaws.com/Prod';

// async function createData() {
//     const data = document.getElementById('createData').value;
//     await sendData('POST', '/students', { data });
//     document.getElementById('result').innerText = 'Data created successfully.';
// }

// async function readData() {
//     const id = document.getElementById('readId').value;
//     await sendData('GET', `/students/${id}`);
//     document.getElementById('result').innerText = 'Data read successfully: ' + responseData;
// }

// async function updateData() {
//     const id = document.getElementById('updateId').value;
//     const data = document.getElementById('updateData').value;
//     await sendData('PUT', `/students/${id}`, { data });
//     document.getElementById('result').innerText = 'Data updated successfully.';
// }

// async function deleteData() {
//     const id = document.getElementById('deleteId').value;
//     await sendData('DELETE', `/students/${id}`);
//     document.getElementById('result').innerText = 'Data deleted successfully.';
// }

// async function sendData(method, path, body) {
//     try {
//         const apiGateway = new AWS.ApiGatewayManagementApi({
//             endpoint: apiEndpoint,
//         });

//         const connectionId = ''; // connection ID

//         const params = {
//             ConnectionId: connectionId,
//             Data: JSON.stringify({
//                 method,
//                 path,
//                 body,
//             }),
//         };

//         await apiGateway.postToConnection(params).promise();
//     } catch (error) {
//         console.error('Error:', error);
//         document.getElementById('result').innerText = 'An error occurred: ' + error.message;
//     }
// }


    // Function to fetch data from DynamoDB
    //async function fetchData() {
    //   try {
    //     // Replace 'YOUR_API_GATEWAY_URL' with the actual URL of your API Gateway
    //     const apiUrl = "https://n2wp9qmj5i.execute-api.us-east-1.amazonaws.com/Prod/students";
        
    //     // Make a GET request to the API Gateway endpoint
    //     const response = await fetch(apiUrl);
        
    //     // Check if the request was successful (status code 200)
    //     if (response.ok) {
    //       // Parse the JSON response
    //       const data = await response.json();
          
    //       // Display the data on the webpage
    //       document.getElementById('data').innerText = JSON.stringify(data, null, 2);
    //     } else {
    //       // Handle error cases
    //       console.error('Failed to fetch data:', response.statusText);
    //     }
    //   } catch (error) {
    //     console.error('Error:', error);
    //   }

      // Use the fetch function to make a GET request to the API endpoint
    //     fetch('https://n2wp9qmj5i.execute-api.us-east-1.amazonaws.com/Prod/students')
    //     .then(function (response) {
    //     // Check if the request was successful (status 200)
    //     if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //     }

    //     // Parse the JSON response
    //     return response.json();
    //     })
    //     .then(function (responseData) {
    //     // Do something with the data
    //     console.log(responseData);
    //     })
    //     .catch(function (error) {
    //     // Handle errors
    //     console.error('Fetch error:', error);
    //     });

    // }

    // Call the fetchData function when the page loads
    //window.onload = fetchData();


    // Use jQuery's AJAX method to fetch data from the API endpoint
  $.ajax({
        url: 'https://dog.ceo/api/breeds/list/all',
        method: 'GET',
        dataType: 'json', // specify the expected data type
        success: function (responseData) {
        // Handle the successful response
        console.log(responseData);

        // Do something with the data
        // For example, update the DOM with the received data
        $('#data').html(JSON.stringify(responseData, null, 2));
        },
        error: function (error) {
        // Handle errors
        console.error('AJAX error:', error);
        }
    });