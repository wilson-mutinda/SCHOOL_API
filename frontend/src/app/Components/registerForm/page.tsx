'use client'
import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import Image from 'next/image'

const RegisterPage = () => {
  const [role, setRole] = useState('')
  const router = useRouter()

  const [close, setClose] = useState(false)

  const handleRoleSelect = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (role === 'parent') {
      router.push('/Components/parentForm') // adjust path as needed
    } else if (role === 'teacher') {
      router.push('/Components/teacherForm')
    } else if (role === 'admin') {
        router.push('/Components/adminForm')
    } else if (role === 'student') {
        router.push('/Components/studentForm') // adjust path as needed
    } else {
      alert('Please select a valid role')
    }
  }

  //   handle close
  const handleClose = async () => {
    setClose(true);
    router.push('/')
}

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-md relative">
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
      <h1 className="text-2xl font-bold mb-4 text-center">Select Role to Register</h1>
      <form onSubmit={handleRoleSelect} className="space-y-4">
        <div>
          <label htmlFor="role" className="block font-medium mb-1">Choose Role</label>
          <select
            id="role"
            name="role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full border border-gray-300 rounded-md p-2"
            required
          >
            <option value="">-- Select Role --</option>
            <option value="parent">Parent</option>
            <option value="teacher">Teacher</option>
            <option value="student">Student</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div className="text-center pt-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Continue
          </button>
        </div>
      </form>
    </div>
  )
}

export default RegisterPage
