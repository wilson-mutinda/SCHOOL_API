'use client'
import React, { use, useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Image from 'next/image'
import Link from 'next/link'
import { deleteAdmin, fetchAdmins } from '@/config/utils'
import { FiArrowLeft } from 'react-icons/fi'

interface Admin {
    id: string,
    first_name: string,
    last_name: string,
    username: string,
    email: string,
    password: string,
    confirm_password: string
}

const AllAdminsPage = () => {

    const [searchQuery, setSearchQuery] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [admins, setAdmins] = useState<Admin[]>([]);
    const [loading, setLoading] = useState(true)

    // fetch all admins
    const loadAdmins = async () => {
        try {
            const data = await fetchAdmins();
            if (data.error) {
                setError(data.error)
            } else {
                setAdmins(data)
            }
        } catch (error) {
            setError('Failed to fetch admins')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadAdmins()
    }, [])

    // handle delete
    const handleDelete = async (id: string) => {
        const isConfirmed = window.confirm("Sure To Delete?")

        if (isConfirmed) {
            try {
                const response = await deleteAdmin(id)
    
                if (response.error) {
                    setError(response.error)
                } else {
                    setError(null);
                    loadAdmins()
                }
            } catch (error: any) {
                setError("Error Deleting Admin")
                loadAdmins();
            }
        }
    }

    // function to filter admins with names
    const filteredAdmins = admins.filter((admin) => admin.first_name.toLowerCase().includes(searchQuery.toLowerCase()) 
        || admin.last_name.toLowerCase().includes(searchQuery.toLowerCase())
        || admin.username.toLowerCase().includes(searchQuery.toLowerCase())
        || admin.email.toLowerCase().includes(searchQuery.toLowerCase())
    )

  return (
    <div className='bg-yellow-100 min-h-screen'>
        {/* LEFT AND RIGHT SECTION */}
        <div className="flex flex-col sm:flex-row min-h-screen">
            {/* LEFT SECTION */}
            <div className="bg-[#dcdcdc] sm:w-[25%] md:w-[20%]">
                <DashboardSideBar/>
            </div>
            {/* RIGHT SECTION */}
            <div className="bg-[#e6e6fa] sm:w-[75%] md:w-[80%]">
            {/* SEARCH BAR AND ADMIN TABLE */}
            <div className="p-4">
                 {/* BACK BUTTON */}
                <Link 
                href="/Components/Dashboard" 
                className="inline-flex items-center space-x-2 mb-2 text-blue-500 hover:text-blue-700 bg-green-500 hover:bg-yellow-300 rounded-lg p-3 transition-all duration-300 shadow-lg transform hover:scale-105"
                >
                <FiArrowLeft className="text-xl" />
                <span className='text-white font-semibold'>Back</span>
                </Link>
                {/* SEARCH BAR */}
                <div className="flex items-center justify-between mb-4">
                <div className="flex items-center ring-2 ring-yellow-300 hover:ring-blue-300 rounded-md p-2 gap-3">
                    <Image src='/search.png' alt='Search' width={20} height={20} className='w-6 h-6'/>
                    <input 
                    type="text" 
                    placeholder="Search Admin.." 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className='outline-none bg-transparent w-full'
                    />
                </div>
                <Link href='/Components/adminForm'>
                    <button className='p-2'>
                    <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8'/>
                    </button>
                </Link>
                </div>
                
                {/* ADMIN TABLE */}
                <div className="overflow-x-auto">
                <table className='w-full border-collapse'>
                    <thead>
                    <tr className='bg-gray-200'>
                        <th className='border border-gray-500 p-2'>#</th>
                        <th className='border border-gray-500 p-2'>FirstName</th>
                        <th className='border border-gray-500 p-2'>LastName</th>
                        <th className='border border-gray-500 p-2'>UserName</th>
                        <th className='border border-gray-500 p-2'>Email</th>
                        <th className='border border-gray-500 p-2'>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {filteredAdmins.map((admins, index) => (
                        <tr key={index} className='hover:bg-gray-50'>
                        <td className='border border-gray-500 p-2'>{index + 1}</td>
                        <td className='border border-gray-500 p-2'>{admins.first_name}</td>
                        <td className='border border-gray-500 p-2'>{admins.last_name}</td>
                        <td className='border border-gray-500 p-2'>{admins.username}</td>
                        <td className='border border-gray-500 p-2'>{admins.email}</td>
                        <td className='border border-gray-500 p-2'>
                            {/* UPDATE AND DELETE */}
                            <div className="flex items-center justify-center gap-3">
                            <Link href={`/Components/adminForm?id=${admins.id}`}>
                                <Image src='/update.png' alt='' width={20} height={20} className='rounded-md bg-blue-400 w-8 h-8 p-2'/>
                            </Link>
                            <button onClick={() => handleDelete(admins.id)}>
                                <Image src='/delete.png' alt='' width={20} height={20} className='rounded-md bg-red-400 w-8 h-8 p-2'/>
                            </button>
                            </div>
                        </td>
                        </tr>
                    ))}
                    {filteredAdmins.length === 0 &&(
                        <tr>
                            <td colSpan={3} className='text-center text-red-500 font-semibold'>No Matching Content</td>
                        </tr>
                    )}
                    </tbody>
                </table>
                </div>
            </div>
            </div>
        </div>
    </div>
  )
}

export default AllAdminsPage