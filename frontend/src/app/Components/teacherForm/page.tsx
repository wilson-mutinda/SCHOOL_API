'use client'
import { createTeacher, singleTeacher, updateTeacher } from '@/config/utils';
import Image from 'next/image';
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react';

const TeacherForm = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [userName, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [profilePicture, setProfilePicture] = useState<File | null>(null);
  const [address, setAddress] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [existingProfilePictureUrl, setExistingProfilePictureUrl] = useState<string | null>(null)

  const [close, setClose] = useState(false);

  const router = useRouter();
  const searchParams = useSearchParams();
  const teacherId = searchParams.get('id');

//   fetch teacher if id exists
useEffect(() => {
    if (teacherId) {
        const fetchTeacher = async () => {
            const {data, error} = await singleTeacher(teacherId);
            if (error) {
                console.error("Error fetching teacher:", error);
                return;
            }
            setFirstName(data.user.first_name || '');
            setLastName(data.user.last_name || "");
            setUsername(data.user.username || '');
            setEmail(data.user.email || '');
            setPhone(data.phone || '');
            setExistingProfilePictureUrl(data.profile_picture || null);
            setAddress(data.address || '');
            setPassword(data.password || '');
            setConfirmPassword(data.confirm_password || '');
        };
        fetchTeacher();
    }
}, [teacherId])

// handle submit
const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();

  if (password && password !== confirmPassword) {
    alert('Passwords do not match!');
    return;
  }

  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Please log in first.');
      return;
    }

    const formData = new FormData();
    
    // Only append fields that are being updated
    if (firstName) formData.append('user.first_name', firstName);
    if (lastName) formData.append('user.last_name', lastName);
    if (userName) formData.append('user.username', userName);
    if (email) formData.append('user.email', email);
    
    if (password) {
      formData.append('user.password', password);
      formData.append('user.confirm_password', confirmPassword);
    }
    
    if (profilePicture) {
      formData.append('profile_picture', profilePicture);
    }
    
    if (phone) formData.append('phone', phone);
    if (address) formData.append('address', address);

    if (teacherId) {
      await updateTeacher(teacherId, formData, token);
      alert('Teacher updated successfully!');
      router.push('/Components/AllTeachers');
    } else {
      // For create, all required fields must be included
      formData.append('user.role.name', 'teacher');
      await createTeacher(
        firstName,
        lastName,
        userName,
        email,
        phone,
        profilePicture as File,
        address,
        password,
        confirmPassword,
        token
      );
      alert('Teacher created successfully!');
      router.push('/Components/Login')
    }
  } catch (error: any) {
    console.error('Detailed error:', error);
    alert(error.message || 'Something went wrong. Please check console for details.');
  }
};

//   handle close
const handleClose = async () => {
    setClose(true);
    router.push('/Components/registerForm')
}

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-2xl rounded-2xl mt-10 relative">
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20}/>
        </button>
      <h2 className="text-2xl font-semibold mb-6 text-center">{teacherId ? 'Teacher Update Form' : 'Teacher Register Form'}</h2>
      <form onSubmit={handleSubmit} encType="multipart/form-data" className="space-y-6">
        {/* First Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label htmlFor="first_name">First Name</label>
            <input
              required 
              type="text"
              name="first_name"
              id="first_name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              placeholder="First Name"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label htmlFor="last_name">Last Name</label>
            <input
              required 
              type="text"
              name="last_name"
              id="last_name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              placeholder="Last Name"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label htmlFor="username">Username</label>
            <input
              required 
              type="text"
              name="username"
              id="username"
              value={userName}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Second Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label htmlFor="email">Email</label>
            <input
              required 
              type="email"
              name="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label htmlFor="phone">Phone</label>
            <input
              required 
              type="tel"
              name="phone"
              id="phone"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Phone"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label htmlFor="profile_picture">Profile Picture</label>
            <input
              required 
              type="file"
              name="profile_picture"
              id="profile_picture"
              onChange={(e) => setProfilePicture(e.target.files?.[0] || null)}
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Address */}
        <div>
          <label htmlFor="address">Address</label>
          <input
            required 
            type="text"
            name="address"
            id="address"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            placeholder="Address"
            className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Passwords */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="password">Password</label>
            <input
              required 
              type="password"
              name="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label htmlFor="confirm_password">Confirm Password</label>
            <input
              required 
              type="password"
              name="confirm_password"
              id="confirm_password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm Password"
              className="mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        {/* Submit */}
        <div className="text-center pt-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
          >
            {teacherId ? 'Update' : 'Register'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TeacherForm;
