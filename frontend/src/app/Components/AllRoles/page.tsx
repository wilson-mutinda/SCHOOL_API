'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Link from 'next/link';
import Image from 'next/image';
import { deleteRole, fetchRoles } from '@/config/utils';
import { useRouter } from 'next/navigation';

interface Role {
  id: string,
  name: string
}

const AllRolesPage = () => {

  const [role, setRole] = useState<Role[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const [searchQuery, setSearchQuery] = useState('');

  const router = useRouter()

  // function to fetch all roles
  const fetchRole = async () => {
    const data = await fetchRoles()
    setRole(data)
  }

  useEffect(() => {
    fetchRole()
  }, []);

  // function to handle delete
  const handleDelete = async (id: string) => {
    const confirmDelete = window.confirm("Sure to delete?");
  
    if (confirmDelete) {
      try {
        const response = await deleteRole(id);
  
        if (response?.error) {
          setError(response.error);  // Show error on UI
        } else {
          setError(null);  // Clear previous error
          fetchRole(); // Refresh roles after successful deletion
        }
  
      } catch (err: any) {
        setError("Failed to delete role.");
      }
    }
  };


  // fetch role using name
  const fetchedRole = role.filter((role_name) => role_name.name.toLowerCase().includes(searchQuery.toLowerCase()))
  
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
          {/* SEARCH BAR AND TEACHER TABLE */}
          <div className="p-4">
            {/* SEARCH BAR */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center ring-2 ring-yellow-300 hover:ring-blue-300 rounded-md p-2 gap-3">
                <Image src='/search.png' alt='Search' width={20} height={20} className='w-6 h-6'/>
                <input 
                  type="text" 
                  placeholder="Search Role..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className='outline-none bg-transparent w-full'
                />
              </div>
              <Link href='/Components/roleForm'>
                <button className='p-2'>
                  <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8'/>
                </button>
              </Link>
            </div>
            
            {/* Role TABLE */}
            <div className="overflow-x-auto">
              <table className='w-full border-collapse'>
                <thead>
                  <tr className='bg-gray-200'>
                    <th className='border border-gray-500 p-2'>#</th>
                    <th className='border border-gray-500 p-2'>Name</th>
                    <th className='border border-gray-500 p-2'>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {fetchedRole.map((role, index) => (
                    <tr key={index} className='hover:bg-gray-50'>
                      <td className='border border-gray-500 p-2'>{index + 1}</td>
                      <td className='border border-gray-500 p-2'>{role.name}</td>
                      <td className='border border-gray-500 p-2'>
                        {/* UPDATE AND DELETE */}
                        <div className="flex items-center justify-center gap-3">
                          <Link href={`/Components/roleForm?id=${role.id}`}>
                            <Image src='/update.png' alt='' width={20} height={20} className='rounded-md bg-blue-400 w-8 h-8 p-2'/>
                          </Link>
                          <button onClick={() => handleDelete(role.id)}>
                            <Image src='/delete.png' alt='' width={20} height={20} className='rounded-md bg-red-400 w-8 h-8 p-2'/>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {fetchedRole.length === 0 && (
                    <tr>
                      <td colSpan={3} className='text-red-500 text-center font-semibold'>No Matching Content!</td>
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

export default AllRolesPage