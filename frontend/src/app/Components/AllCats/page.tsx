'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Link from 'next/link';
import Image from 'next/image';
import { deleteCat, deleteExam, fetchCats, fetchExams } from '@/config/utils';
import { FiArrowDownCircle, FiArrowDownLeft, FiArrowLeft, FiBarChart, FiSkipBack } from 'react-icons/fi';

interface Cat {
  id: string,
  cat_name: string,
  cat_code: string,
  subject: string,
  content: string,
  date_done: string,
  start_time: string,
  cat_term: string,
}

const AllCatsPage = () => {
  
  const [cats, setCats] = useState<Cat[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  // handle fetch
  const fetchCat = async () => {
    const data = await fetchCats();
    if (data.error) {
      setError(data.error);
      return;
    }
    setCats(data)
  }

  useEffect(() => {
    fetchCat()
  }, []);

  // handle delete
  const handleDelete = async (id: string) => {

    const confirmDelete = window.confirm("Delete Cat?");

    if (confirmDelete) {
      const response = await deleteCat(id);
      if (response.error) {
        setError(response.error);
        return;
      }
      alert("Cat Deleted Successfully");
      fetchCat()
    }
  }

  // filter by name, cat code, subject and date, and term
  const filteredCats = cats.filter((cat) => cat.date_done.toLowerCase().includes(searchQuery.toLowerCase())
   || cat.cat_code.toLowerCase().includes(searchQuery.toLowerCase()) || cat.cat_name.toLowerCase().includes(searchQuery.toLowerCase()) 
   || cat.subject.toLowerCase().includes(searchQuery.toLowerCase()) || cat.cat_term.toLowerCase().includes(searchQuery.toLowerCase()))

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
                  placeholder="Search Cat..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className='outline-none bg-transparent w-full'
                />
              </div>
              <Link href='/Components/catGradeForm'>
                <button className='p-2 rounded-md bg-blue-500'>
                  Grade Cat
                </button>
              </Link>
              <Link href='/Components/catForm'>
                <button className='p-2'>
                  <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8'/>
                </button>
              </Link>
            </div>         
            {/* CAT TABLE */}
            <div className="overflow-x-auto">
              <table className='w-full border-collapse'>
                <thead>
                  <tr className='bg-gray-200'>
                    <th className='border border-gray-500 p-2'>#</th>
                    <th className='border border-gray-500 p-2'>Cat Name</th>
                    <th className='border border-gray-500 p-2'>Cat Code</th>
                    <th className='border border-gray-500 p-2'>Subject</th>
                    <th className='border border-gray-500 p-2'>Content</th>
                    <th className='border border-gray-500 p-2'>Date</th>
                    <th className='border border-gray-500 p-2'>StartTime</th>
                    <th className='border border-gray-500 p-2'>Term</th>
                    <th className='border border-gray-500 p-2'>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCats.map((cat, index) => (
                    <tr key={cat.id}>
                      <td className='border border-gray-500 p-2'>{index + 1}</td>
                      <td className='border border-gray-500 p-2'>{cat.cat_name}</td>
                      <td className='border border-gray-500 p-2'>{cat.cat_code}</td>
                      <td className='border border-gray-500 p-2'>{cat.subject}</td>
                      <td className='border border-gray-500 p-2'>{cat.content}</td>
                      <td className='border border-gray-500 p-2'>{cat.date_done}</td>
                      <td className='border border-gray-500 p-2'>{cat.start_time}</td>
                      <td className='border border-gray-500 p-2'>{cat.cat_term}</td>
                      <td className='border border-gray-500 p-2'>
                        {/* UPDATE AND DELETE */}
                        <div className="flex items-center justify-center gap-3">
                          <Link href={`/Components/catForm?id=${cat.id}`}>
                            <Image src='/update.png' alt='' width={20} height={20} className='rounded-md bg-blue-400 w-8 h-8 p-2' />
                          </Link>
                          <button onClick={() => handleDelete(cat.id)}>
                            <Image src='/delete.png' alt='' width={20} height={20} className='rounded-md bg-red-400 w-8 h-8 p-2'/>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {filteredCats.length === 0 && (
                    <tr>
                      <td className='text-red-600 font-bold text-center' colSpan={3}>No Matching Content!</td>
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

export default AllCatsPage