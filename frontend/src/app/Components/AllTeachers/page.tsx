'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Image from 'next/image'
import Link from 'next/link'
import { deleteTeacher, fetchTeachers } from '@/config/utils'
import { FiArrowLeft } from 'react-icons/fi'

interface User {
  first_name: string;
  last_name: string;
  username: string;
  email: string;
}

interface Teacher {
  id: number;
  user: User;
  phone: string;
  address: string;
  teacher_code: string;
  profile_picture?: string;
}

const AllTeachersPage = () => {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    const { data, error } = await fetchTeachers();
    
    if (error) {
      setError(error);
    } else {
      setTeachers(data);
    }
    
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="bg-yellow-100 min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full border-blue-400 w-12 h-12 border-b-2"></div>
      </div>
    );
  }

  // handle delete 
  const handleDelete = async (id: number) => {
    const confirmDelete = confirm("Are you sure you want to delete this teacher?");
    if (!confirmDelete) return;
  
    try {
      await deleteTeacher(String(id));
      // Refresh the list after deletion
      fetchData();
    } catch (error) {
      console.error("Delete failed", error);
      setError("Failed to delete teacher.");
    }
  };  

  return (
    <div className='bg-yellow-100 min-h-screen'>
      {/* Error display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role='alert'>
          <strong className='font-bold'>Error! </strong>
          <span className='block sm:inline'>{error}</span>
        </div>
      )}
      
      <div className="flex flex-col sm:flex-row min-h-screen">
        {/* LEFT SECTION */}
        <div className="bg-[#dcdcdc] sm:w-[25%] md:w-[20%]">
          <DashboardSideBar/>
        </div>
        
        {/* RIGHT SECTION */}
        <div className="bg-[#e6e6fa] sm:w-[75%] md:w-[80%]">
          {/* SEARCH BAR AND TEACHER TABLE */}
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
                  placeholder="Search Teacher..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className='outline-none bg-transparent w-full'
                />
              </div>
              <Link href='/Components/teacherForm'>
                <button className='p-2'>
                  <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8'/>
                </button>
              </Link>
            </div>
            
            {/* TEACHER TABLE */}
            <div className="overflow-x-auto">
              <table className='w-full border-collapse'>
                <thead>
                  <tr className='bg-gray-200'>
                    <th className='border border-gray-500 p-2'>ID</th>
                    <th className='border border-gray-500 p-2'>First Name</th>
                    <th className='border border-gray-500 p-2'>Last Name</th>
                    <th className='border border-gray-500 p-2'>Username</th>
                    <th className='border border-gray-500 p-2'>Email</th>
                    <th className='border border-gray-500 p-2'>Phone</th>
                    <th className='border border-gray-500 p-2'>Profile</th>
                    <th className='border border-gray-500 p-2'>Address</th>
                    <th className='border border-gray-500 p-2'>Teacher Code</th>
                    <th className='border border-gray-500 p-2'>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {teachers
                  .filter((teacher) => {
                    const fullName = `${teacher.user.first_name} ${teacher.user.last_name}`.toLowerCase();
                    const username = teacher.user.username.toLowerCase();
                    const email = teacher.user.email.toLowerCase();
                    const query = searchQuery.toLowerCase();

                    return (
                      fullName.includes(query) ||
                      username.includes(query) ||
                      email.includes(query)
                    );
                  })
                  .map((teacher, index) => (
                    <tr key={index} className='hover:bg-gray-50'>
                      <td className='border border-gray-500 p-2 text-center'>{index + 1}</td>
                      <td className='border border-gray-500 p-2'>{teacher.user?.first_name}</td>
                      <td className='border border-gray-500 p-2'>{teacher.user?.last_name}</td>
                      <td className='border border-gray-500 p-2'>{teacher.user?.username}</td>
                      <td className='border border-gray-500 p-2'>{teacher.user?.email}</td>
                      <td className='border border-gray-500 p-2'>{teacher.phone}</td>
                      <td className='border border-gray-500 p-2 text-center'>
                        {teacher.profile_picture ? (
                          <div className="p-1 border border-gray-300 rounded-lg inline-block shadow-sm">
                            <Image
                              src={teacher.profile_picture}
                              alt={`${teacher.user.first_name} profile`}
                              width={40}
                              height={40}
                              unoptimized
                              className='rounded-lg'
                            />
                          </div>
                        ) : (
                          <span className="text-gray-400 italic">No image</span>
                        )}
                      </td>
                      <td className='border border-gray-500 p-2'>{teacher.address}</td>
                      <td className='border border-gray-500 p-2'>{teacher.teacher_code}</td>
                      <td className='border border-gray-500 p-2'>
                        {/* UPDATE AND DELETE */}
                        <div className="flex items-center justify-center gap-3">
                          <Link href={`/Components/teacherForm?id=${teacher.id}`}>
                            <Image src='/update.png' alt='' width={20} height={20} className='rounded-md bg-blue-400 w-8 h-8 p-2'/>
                          </Link>
                          <button onClick={() => handleDelete(teacher.id)}>
                            <Image src='/delete.png' alt='' width={20} height={20} className='rounded-md bg-red-400 w-8 h-8 p-2'/>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AllTeachersPage;