// AWS SDK Configuration
AWS.config.update({
    region: 'us-east-1',
});

// API Gateway endpoint
const apiEndpoint = 'https://oyofa5d7gk.execute-api.us-east-1.amazonaws.com/Prod/';

async function createData() {
    const data = document.getElementById('createData').value;
    await sendData('POST', '/create', { data });
}

async function readData() {
    const id = document.getElementById('readId').value;
    await sendData('GET', `/read/${id}`);
}

async function updateData() {
    const id = document.getElementById('updateId').value;
    const data = document.getElementById('updateData').value;
    await sendData('PUT', `/update/${id}`, { data });
}

async function deleteData() {
    const id = document.getElementById('deleteId').value;
    await sendData('DELETE', `/delete/${id}`);
}

async function sendData(method, path, body) {
    try {
        const apiGateway = new AWS.ApiGatewayManagementApi({
            endpoint: apiEndpoint,
        });

        const connectionId = 'YOUR_CONNECTION_ID'; // Replace with the actual connection ID

        const params = {
            ConnectionId: connectionId,
            Data: JSON.stringify({
                method,
                path,
                body,
            }),
        };

        await apiGateway.postToConnection(params).promise();
    } catch (error) {
        console.error('Error:', error);
    }
}