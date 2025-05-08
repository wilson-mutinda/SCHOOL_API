'use client'
import React, { useEffect, useState } from 'react'
import DashboardSideBar from '../dashboard_sidebar/page'
import Link from 'next/link';
import Image from 'next/image';
import { deleteCatGrade, deleteExam, deleteExamGrade, fetchCatGrades, fetchExamGrades, fetchExams } from '@/config/utils';
import { FiArrowLeft } from 'react-icons/fi';

interface CatGrade {
  id: string,
  cat_name: string,
  student: string,
  subject: string,
  marks: string,
  grade: string,
}

const AllCatGradesPage = () => {
  
  const [catGrades, setCatGrades] = useState<CatGrade[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  // handle fetch
  const fetchCatGrade = async () => {
    const data = await fetchCatGrades();
    if (data.error) {
      setError(data.error);
      return;
    }
    setCatGrades(data)
  }

  useEffect(() => {
    fetchCatGrade()
  }, []);

  // handle delete
  const handleDelete = async (id: string) => {

    const confirmDelete = window.confirm("Delete CatGrade?");

    if (confirmDelete) {
      const response = await deleteCatGrade(id);
      if (response.error) {
        setError(response.error);
        return;
      }
      alert("CatGrade Deleted Successfully");
      fetchCatGrade()
    }
  }

  // filter by name, exam code, subject and date, and term
  const filteredCatGrades = catGrades.filter((catGrade) => catGrade.cat_name.toLowerCase().includes(searchQuery.toLowerCase())
   || catGrade.student.toLowerCase().includes(searchQuery.toLowerCase()) || catGrade.subject.toLowerCase().includes(searchQuery.toLowerCase()))

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
                  placeholder="Search CatGrade..." 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className='outline-none bg-transparent w-full'
                />
              </div>
              <Link href='/Components/catGradeForm'>
                <button className='p-2'>
                  <Image src='/create.png' alt='Create' width={20} height={20} className='rounded-full bg-yellow-400 h-8 w-8'/>
                </button>
              </Link>
            </div>
            
            {/* EXAM Grading TABLE */}
            <div className="overflow-x-auto">
              <table className='w-full border-collapse'>
                <thead>
                  <tr className='bg-gray-200'>
                    <th className='border border-gray-500 p-2'>#</th>
                    <th className='border border-gray-500 p-2'>Cat</th>
                    <th className='border border-gray-500 p-2'>Student</th>
                    <th className='border border-gray-500 p-2'>Subject</th>
                    <th className='border border-gray-500 p-2'>Marks</th>
                    <th className='border border-gray-500 p-2'>Grade</th>
                    <th className='border border-gray-500 p-2'>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCatGrades.map((catGrade, index) => (
                    <tr key={catGrade.id}>
                      <td className='border border-gray-500 p-2'>{index + 1}</td>
                      <td className='border border-gray-500 p-2'>{catGrade.cat_name}</td>
                      <td className='border border-gray-500 p-2'>{catGrade.student}</td>
                      <td className='border border-gray-500 p-2'>{catGrade.subject}</td>
                      <td className='border border-gray-500 p-2'>{catGrade.marks}</td>
                      <td className='border border-gray-500 p-2'>{catGrade.grade}</td>
                      <td className='border border-gray-500 p-2'>
                        {/* UPDATE AND DELETE */}
                        <div className="flex items-center justify-center gap-3">
                          <Link href={`/Components/catGradeForm?id=${catGrade.id}`}>
                            <Image src='/update.png' alt='' width={20} height={20} className='rounded-md bg-blue-400 w-8 h-8 p-2' />
                          </Link>
                          <button onClick={() => handleDelete(catGrade.id)}>
                            <Image src='/delete.png' alt='' width={20} height={20} className='rounded-md bg-red-400 w-8 h-8 p-2'/>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {filteredCatGrades.length === 0 && (
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

export default AllCatGradesPage