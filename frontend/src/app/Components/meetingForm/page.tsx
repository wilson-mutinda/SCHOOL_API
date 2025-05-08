'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { FiX } from 'react-icons/fi'; // adjust the import path as needed
import { createZoomMeeting } from '@/config/utils';

const ZoomMeetingForm = () => {
  const router = useRouter();

  const [meetingInfo, setMeetingInfo] = useState<null | {
    join_url: string;
    meeting_id: number;
    password: string;
  }>(null);  

  const [formData, setFormData] = useState({
    topic: '',
    duration: 30,
    start_date: '',
    start_time: '09:00:00'
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration' ? parseInt(value) : value
    }));
  };

  const handleClose = () => {
    router.push('/Components/Dashboard'); // Redirect to dashboard
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
  
    const { topic, duration, start_date, start_time } = formData;
  
    // Step 1: Check if the selected date is not in the past
    const currentDate = new Date(); // Get current date
    const selectedDate = new Date(start_date);
  
    // Reset time for both currentDate and selectedDate to compare only the date part
    currentDate.setHours(0, 0, 0, 0); // Set current time to 00:00:00
    selectedDate.setHours(0, 0, 0, 0); // Set the selected date's time to 00:00:00
  
    // Now we compare dates directly, as both are now valid Date objects with time set to midnight
    if (selectedDate < currentDate) {
      setError("Start date cannot be in the past.");
      setIsSubmitting(false);
      return;
    }
  
    // Step 2: Check if the selected time is not earlier than the current time
    const selectedDateTime = new Date(`${start_date}T${start_time}`);
    const currentTime = new Date();
  
    if (selectedDateTime < currentTime) {
      setError("Start time cannot be earlier than the current time.");
      setIsSubmitting(false);
      return;
    }
  
    // Proceed with creating the meeting if validation passes
    const response = await createZoomMeeting(topic, duration, start_date, start_time);
  
    if (response?.error) {
      setError(response.error);
    } else {
      setMeetingInfo({
        join_url: response.join_url,
        meeting_id: response.meeting_id,
        password: response.password
      });
    }
  
    setIsSubmitting(false);
  };  

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Create Zoom Meeting</h2>
          <button onClick={handleClose} className="text-gray-500 hover:text-gray-700">
            <FiX size={24} />
          </button>
        </div>

        {error && <p className="text-red-600 mb-2 text-sm">{error}</p>}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Topic</label>
            <input
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Duration (minutes)</label>
            <input
              type="number"
              name="duration"
              value={formData.duration}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Start Date</label>
            <input
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700">Start Time</label>
            <input
              type="time"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              required
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
          >
            {isSubmitting ? 'Creating...' : 'Create Meeting'}
          </button>
        </form>
      </div>
      {meetingInfo && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-sm">
            <h3 className="text-lg font-semibold mb-4">Meeting Created</h3>
            
            <p className="text-sm mb-1"><strong>Title:</strong> {formData.topic}</p>
            <p className="text-sm mb-1"><strong>Date:</strong> {formData.start_date}</p>
            <p className="text-sm mb-3"><strong>Time:</strong> {formData.start_time}</p>

            <p className="text-sm mb-1"><strong>Join URL:</strong> <a href={meetingInfo.join_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">{meetingInfo.join_url}</a></p>
            <p className="text-sm mb-1"><strong>Meeting ID:</strong> {meetingInfo.meeting_id}</p>
            <p className="text-sm mb-4"><strong>Password:</strong> {meetingInfo.password}</p>

            <button
                onClick={() => {
                setMeetingInfo(null);
                router.push('/Components/Dashboard');
                }}
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
            >
                Go to Dashboard
            </button>
            </div>
        </div>
        )}
    </div>
  );
};

export default ZoomMeetingForm;
