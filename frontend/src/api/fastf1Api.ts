export async function getFastestLap() {
  const response = await fetch('http://127.0.0.1:5000/fastest-lap');
  if (!response.ok) throw new Error('Failed to fetch fastest lap');
  return await response.json();
}