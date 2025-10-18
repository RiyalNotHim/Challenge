const { MongoClient } = require('mongodb');

const uri = 'mongodb+srv://csattyam:sattyam16@50projectschallenge.sy0nmkc.mongodb.net/?retryWrites=true&w=majority&appName=50ProjectsChallenge';

let cachedClient = null;

async function connectToDatabase() {
  if (cachedClient) {
    return cachedClient;
  }

  const client = new MongoClient(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  await client.connect();
  cachedClient = client;
  return client;
}

exports.handler = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false;

  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    const client = await connectToDatabase();
    const database = client.db('50projectschallenge');
    const feedbacks = database.collection('feedbacks');

    if (event.httpMethod === 'POST') {
      const { name, comment, day, projectName } = JSON.parse(event.body);
      
      if (!name || !comment || !day) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ error: 'Missing required fields' })
        };
      }
      
      const feedback = {
        name,
        comment,
        day: parseInt(day),
        projectName,
        timestamp: new Date()
      };
      
      const result = await feedbacks.insertOne(feedback);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          success: true, 
          message: 'Feedback submitted successfully',
          id: result.insertedId
        })
      };
    }

    if (event.httpMethod === 'GET') {
      const day = event.queryStringParameters?.day;
      
      const query = day ? { day: parseInt(day) } : {};
      const allFeedbacks = await feedbacks
        .find(query)
        .sort({ timestamp: -1 })
        .toArray();
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(allFeedbacks)
      };
    }

    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };

  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Failed to process request', 
        details: error.message 
      })
    };
  }
};