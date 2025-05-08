'use client'
import React, { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Image from 'next/image'
import { createStudent, singleStudent, updateStudent} from '@/config/utils'

const StudentForm = () => {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [userName, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [parentEmail, setParentEmail] = useState('')
  const [parentCode, setParentCode] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const router = useRouter()
  const searchParams = useSearchParams()
  const studentId = searchParams.get('id')

  useEffect(() => {
    if (studentId) {
      const fetchStudent = async () => {
        try {
          const data = await singleStudent(studentId)
          setFirstName(data.user.first_name || '')
          setLastName(data.user.last_name || '')
          setUsername(data.user.username || '')
          setEmail(data.user.email || '')
          setParentEmail(data.parent_email || '')
          setParentCode(data.parent_code || '')
        } catch (err) {
          console.error("Failed to fetch student data:", err)
        }
      }

      fetchStudent()
    }
  }, [studentId])

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  
    if (!studentId && password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
  
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        alert('Please login first.');
        return;
      }
  
      const payload: any = {
        user: {
          first_name: firstName,
          last_name: lastName,
          username: userName,
          email: email,
          ...(password && {
            password: password,
            confirm_password: confirmPassword,
          }),
        },
        parent_email: parentEmail,
        parent_code: parentCode,
      };
  
      if (!studentId) {
        await createStudent(payload, token);
        alert('Student created successfully!');
        router.push('/Components/Login')
      } else {
        await updateStudent(studentId, payload, token);
        alert('Student updated successfully!');
        router.push('/Components/AllStudents');
      }
    } catch (error: any) {
      console.error('Detailed error:', error);
      alert(error.response?.data?.message || error.message || 'Something went wrong.');
    }
  };
  

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-2xl rounded-2xl mt-10 relative">
      <button onClick={() => router.push('/Components/registerForm')} className="absolute right-3 top-2 rounded-full bg-red-500 p-2">
        <Image src="/close.png" alt="" width={20} height={20} />
      </button>
      <h2 className="text-2xl font-semibold mb-6 text-center">
        {studentId ? 'Update Student' : 'Register Student'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label>First Name</label>
            <input required value={firstName} onChange={e => setFirstName(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
          </div>
          <div>
            <label>Last Name</label>
            <input required value={lastName} onChange={e => setLastName(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
          </div>
          <div>
            <label>Username</label>
            <input required value={userName} onChange={e => setUsername(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label>Email</label>
            <input required type="email" value={email} onChange={e => setEmail(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
          </div>
          <div>
            <label>Parent Email</label>
            <input value={parentEmail} onChange={e => setParentEmail(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
          </div>
          <div>
            <label>Parent Code</label>
            <input value={parentCode} onChange={e => setParentCode(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
          </div>
          {!studentId && (
            <>
              <div>
                <label>Password</label>
                <input required type="password" value={password} onChange={e => setPassword(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
              </div>
              <div>
                <label>Confirm Password</label>
                <input required type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} className="mt-1 block w-full border rounded-md p-2" />
              </div>
            </>
          )}
        </div>
        <div className="text-center">
          <button type="submit" className="bg-yellow-500 hover:bg-yellow-600 px-6 py-2 rounded-lg text-white">
            {studentId ? 'Update' : 'Register'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default StudentForm
