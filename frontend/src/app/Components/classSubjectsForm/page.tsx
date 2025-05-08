'use client'
import { createCat, createExam, createStreamClassSubject, singleCat, singleExam, singleStreamClassSubject, updateCat, updateExam, updateStreamClassSubject } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const classSubjectForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    const [studentCode, setStudentCode] = useState('');
    const [studentClass, setStudentClass] = useState('');
    const [studentStream, setStudentStream] = useState('');

    // get cat id from url
    const searchParams = useSearchParams();
    const classSubjectId = searchParams.get('id');

    // fetch exam id
    useEffect(() => {
        const fetchSingleClassSubject = async () => {
            if (classSubjectId ){
                const data = await singleStreamClassSubject(classSubjectId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setStudentCode(data.student_code || '');
                setStudentClass(data.student_class || '');
                setStudentStream(data.student_stream || '');
            }
        }
        fetchSingleClassSubject();
    }, [classSubjectId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    
        if (classSubjectId) {
            const response = await updateStreamClassSubject(classSubjectId, studentCode, studentClass, studentStream);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Class subject Updated Successfully!");
            router.push('/Components/AllClassSubjects');
        } else {
            const response = await createStreamClassSubject(studentCode, studentClass, studentStream);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Class Subject Created Successfully!");
            router.push('/Components/AllClassSubjects');
        }
    };    

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllClassSubjects')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{classSubjectId ? "Update Class Subject" : "Create Class Suject"}</h2>
            {/* Row 1: Exam name and subject */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div className="">
                    <label htmlFor="exam_name" className='block mb-1 font-medium'>Student Code</label>
                    <input type="text" name="exam_name" value={studentCode} onChange={(e) => setStudentCode(e.target.value)} placeholder="S-002" className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-400' />
                </div>
            </div>

            {/* Row 3:Class and Stream */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div className="">
                    <label htmlFor="exam_class" className='block mb-1 font-medium'>Class</label>
                    <select name="exam_class" id="exam_class" value={studentClass} onChange={(e) => setStudentClass(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Class</option>
                        <option value="F1">F1</option>
                        <option value="F2">F2</option>
                        <option value="F3">F3</option>
                        <option value="F4">F4</option>
                    </select>
                </div>

                <div className="">
                    <label htmlFor="exam_stream" className='block mb-1 font-medium'>Stream</label>
                    <select name="exam_stream" id="exam_stream" value={studentStream} onChange={(e) => setStudentStream(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Stream</option>
                        <option value="w">W</option>
                        <option value="e">E</option>
                    </select>
                </div>
            </div>
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {classSubjectId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default classSubjectForm