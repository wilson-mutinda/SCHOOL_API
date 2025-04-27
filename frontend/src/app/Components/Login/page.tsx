'use client'
import { loginUser } from '@/config/utils'
import Image from 'next/image'
import { useRouter } from 'next/navigation'
import React, { useState } from 'react'

const loginPage = () => {
    const [close, setClose] = useState(false)

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const router = useRouter()

    // function to close
    const handleClose = async () => {
      setClose(true)
      router.push('/')
    }

    // Const handle login
    const handleLogin = async (e:React.FormEvent) => {
      e.preventDefault();

      const result = await loginUser(email, password);

      if (result.success) {
        router.push('/Components/Dashboard')
      } else {
        alert(result.error || 'Login Failed')
      }
    };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-yellow-100 to-blue-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md relative">
        <button onClick={handleClose} className='w-6 h-6 absolute top-1 right-1'>
            <Image src='/close.png' alt='' width={20} height={20} className='rounded-full bg-red-500'/>
        </button>
        <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Login to Bidii High School</h2>
        <form className="space-y-4" onSubmit={handleLogin}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e)=> setPassword(e.target.value)}
              placeholder="Enter your password"
              className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-2 rounded-md"
          >
            Login
          </button>
          <p className="text-center text-sm mt-2">
            Don’t have an account? <a href="/register" className="text-blue-600 underline">Register</a>
          </p>
        </form>
      </div>
    </div>
  )
}

export default loginPage