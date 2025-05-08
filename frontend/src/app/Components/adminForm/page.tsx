'use client'
import { createAdmin, singleAdmin, updateAdmin } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const AdminForm = () => {

  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('')

  const [close, setClose] = useState(false);
  const router = useRouter()

  // get id from the url
  const searchParams = useSearchParams()
  const adminId = searchParams.get('id');

  // use effect to fetch an admin with an admin id
  useEffect(() => {
    if (adminId) {
      const adminInfo = async () => {
        const data = await singleAdmin(adminId)
        setFirstName(data.first_name || '');
        setLastName(data.last_name || '');
        setUsername(data.username || '');
        setEmail(data.email || '');
        setPassword(data.password || '');
        setConfirmPassword(data.confirm_password || '');
      };
      adminInfo();
    }
  }, [adminId])

  // handle submit
  const handleSubmit = async (e:React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      if (password && password !== confirmPassword) {
        alert("Password Mismatch!")
        return
      }
  
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('Login Required!');
        return;
      }
      
      if (adminId) {
        // update mode
        const response = await updateAdmin( adminId, first_name, last_name, username, email, password, confirmPassword, token);
        if (response.error) {
          alert(response.error)
          return;
        }
        alert ("Admin Updated Successfully");
        router.push('/Components/AllAdmins')
      } else {
        // Create mode
        const response = await createAdmin(first_name, last_name, username, email, password, confirmPassword, token);
        if (response.error) {
          alert(response.error);
          return;
        }
        alert ('Admin Created Successfully!')
        router.push('/Components/Login')
      }
    } catch (error: any) {
      console.error("Unknown Error", error);
      alert(error.message || "Something Went Wrong")
    }
  };

  //   handle close
  const handleClose = async () => {
    setClose(true);
    router.push('/Components/registerForm')
}
  return (
    <div className='max-w-4xl mx-auto p-6 bg-white shadow-2xl rounded-2xl mt-10 relative'>
      <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
          <Image src='/close.png' alt='' width={20} height={20} />
      </button>
      <h2 className="text-2xl font-semibold mb-6 text-center">{adminId ? "Admin Update Form" : "Admin Register Form"}</h2>
      <form onSubmit={handleSubmit} method="post">
        <div className="grid grid-cols-2 gap-3">
          <div className="">
            <label htmlFor="firstName" className='font-semibold'>FirstName</label>
            <input 
              required
              type="text" 
              value={first_name}
              onChange={(e) => setFirstName(e.target.value)}
              name="first_name" 
              placeholder="FirstName" 
              className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
          </div>
          <div className="lastName">
            <label className='font-semibold' htmlFor="lastName">LastName</label>
            <input
             required 
             type="text" 
             value={last_name}
             onChange={(e) => setLastName(e.target.value)}
             name="last_name" 
             placeholder="LastName" 
             className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="">
            <label className='font-semibold' htmlFor="userName">UserName</label>
            <input
             required 
             type="text" 
             value={username}
             onChange={(e) => setUsername(e.target.value)}
             name="username" 
             placeholder="UserName" 
             className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
          </div>
          <div className="">
            <label className='font-semibold' htmlFor="Email">Email</label>
            <input
             required 
             type="email" 
             value={email}
             onChange={(e) => setEmail(e.target.value)}
             name="email" 
             placeholder="Email" 
             className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div className="">
            <label className='font-semibold' htmlFor="password">Password</label>
            <input
             required 
             type="password" 
             value={password}
             onChange={(e) => setPassword(e.target.value)}
             name="password" 
             placeholder="password" 
             className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
          </div>
          <div className="">
            <label className='font-semibold' htmlFor="confirm_password">Confirm Password</label>
            <input
             required 
             type="password" 
             value={confirmPassword}
             onChange={(e) => setConfirmPassword(e.target.value)}
             name="confirm_password" 
             placeholder="Confirm_password" 
             className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
          </div>
        </div>
        {/* submit */}
        <div className="text-center pt-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
          >
            {adminId ? "Update" : "Create"}
          </button>
        </div>
      </form>
    </div>
  )
}

export default AdminForm