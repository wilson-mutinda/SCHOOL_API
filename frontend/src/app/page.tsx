'use client'
import React from 'react'
import Link from 'next/link'

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-50 to-yellow-100 text-gray-800">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 bg-yellow-400 shadow-md">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">🏫 Bidii High School</h1>
          <p className="text-sm text-gray-700">"Knowledge is Power, Discipline is Key"</p>
        </div>
        <Link href="/Components/registerForm">
          <button className="bg-white text-yellow-600 font-semibold px-4 py-2 rounded shadow hover:bg-yellow-100 transition">
            Register
          </button>
        </Link>
        <Link href="/Components/Login">
          <button className="bg-white text-yellow-600 font-semibold px-4 py-2 rounded shadow hover:bg-yellow-100 transition">
            Login
          </button>
        </Link>
      </header>

      {/* Main Content */}
      <main className="p-6 max-w-6xl mx-auto">
        {/* Hero Section */}
        <section className="flex flex-col md:flex-row items-center justify-between mt-16 mb-10">
          <div className="md:w-1/2 mb-10 md:mb-0 text-center md:text-left">
            <h2 className="text-4xl font-semibold mb-4">Welcome to Bidii High School</h2>
            <p className="text-lg mb-6">
              We nurture young minds with quality education, strong moral values, and a drive for excellence.
            </p>
            <Link href="/Components/registerForm">
              <button className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold px-6 py-3 rounded-lg transition">
                Get Started
              </button>
            </Link>
          </div>
          <div className="md:w-1/2">
            <img
              src="/school_building.png"
              alt="School"
              className="w-full rounded-lg shadow-lg"
            />
          </div>
        </section>

        {/* About Section */}
        <section className="bg-white p-6 rounded-lg shadow-md mt-12">
          <h3 className="text-2xl font-bold mb-3">About Us</h3>
          <p className="text-gray-700">
            Bidii High School is committed to offering a conducive learning environment with well-trained staff, state-of-the-art facilities, and a curriculum designed to inspire academic and personal growth.
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-4 text-center">
        © {new Date().getFullYear()} Bidii High School. All rights reserved.
      </footer>
    </div>
  )
}

export default HomePage
