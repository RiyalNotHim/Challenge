const { neon } = require('@neondatabase/serverless');

const connectionString = 'postgresql://neondb_owner:npg_wL4NkvmciW6u@ep-wandering-lab-a13oheum-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require';

const sql = neon(connectionString);

async function initializeDatabase() {
  await sql`
    CREATE TABLE IF NOT EXISTS feedbacks (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      comment TEXT NOT NULL,
      day INTEGER NOT NULL,
      project_name VARCHAR(255),
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `;
  
  await sql`
    CREATE INDEX IF NOT EXISTS idx_feedbacks_day ON feedbacks(day)
  `;
}

exports.handler = async (event, context) => {
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
    await initializeDatabase();

    if (event.httpMethod === 'POST') {
      const { name, comment, day, projectName } = JSON.parse(event.body);
      
      if (!name || !comment || !day) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ error: 'Missing required fields' })
        };
      }
      
      const result = await sql`
        INSERT INTO feedbacks (name, comment, day, project_name)
        VALUES (${name}, ${comment}, ${parseInt(day)}, ${projectName || null})
        RETURNING id
      `;
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ 
          success: true, 
          message: 'Feedback submitted successfully',
          id: result[0].id
        })
      };
    }

    if (event.httpMethod === 'GET') {
      const day = event.queryStringParameters?.day;
      
      let feedbacks;
      if (day) {
        feedbacks = await sql`
          SELECT id, name, comment, day, project_name, timestamp
          FROM feedbacks
          WHERE day = ${parseInt(day)}
          ORDER BY timestamp DESC
        `;
      } else {
        feedbacks = await sql`
          SELECT id, name, comment, day, project_name, timestamp
          FROM feedbacks
          ORDER BY timestamp DESC
        `;
      }
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(feedbacks)
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