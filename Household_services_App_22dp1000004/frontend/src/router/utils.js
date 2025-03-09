import axios from 'axios';

export async function getUserName() {
  console.log(localStorage);
  let userName = localStorage.getItem('username');
  console.log('userName', userName);
  const token = localStorage.getItem('token');

  if (!userName && token) {
    try {
      const response = await axios.get('http://127.0.0.1:5858/auth/profile', {
        headers: { Authorization: `Bearer ${token}` }
      });

      userName = response.data.name; // API returns { "name": "user name" }
      localStorage.setItem('username', userName); // Store in localStorage
    } catch (error) {
      console.error('Error fetching user name:', error);
    }
  }

  return userName || 'Unknown User'; // Fallback if name isn't found
}
