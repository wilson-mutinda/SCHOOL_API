import Link from 'next/link'
import React from 'react'
import { FiArrowLeft } from 'react-icons/fi'

const AboutPage = () => {
  return (
    <div className="p-8 bg-white shadow rounded-lg">
        {/* BACK BUTTON */}
        <Link 
                href="/Components/Dashboard" 
                className="inline-flex items-center space-x-2 mb-2 text-blue-500 hover:text-blue-700 bg-green-500 hover:bg-yellow-300 rounded-lg p-3 transition-all duration-300 shadow-lg transform hover:scale-105"
                >
                <FiArrowLeft className="text-xl" />
                <span className='text-white font-semibold'>Back</span>
                </Link>
      <h1 className="text-3xl font-bold mb-4 text-blue-600">About Bidii School LSM</h1>
      <p className="text-gray-700 text-lg">
        The Bidii School Learning Support Management (LSM) system is designed to help students,
        teachers, and administrators track learning progress, manage assignments, and support
        academic growth in an organized and efficient manner. Our platform promotes collaboration,
        timely feedback, and easy access to educational resources.
      </p>
      <p className="text-gray-600 mt-4">
        Whether you're a student looking to check your progress, or a teacher managing learning plans,
        Bidii School LSM is built to make learning better for everyone.
      </p>
    </div>
  )
}

export default AboutPage
