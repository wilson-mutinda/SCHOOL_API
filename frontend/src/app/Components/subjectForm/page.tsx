'use client'
import { createExam, createSubject, singleExam, singleSubject, updateExam, updateSubject } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const subjectForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    const [subjectName, setSubjectName] = useState('');

    // get subject id from url
    const searchParams = useSearchParams();
    const subjectId = searchParams.get('id');

    // fetch subject id
    useEffect(() => {
        const fetchSingleSubject = async () => {
            if (subjectId ){
                const data = await singleSubject(subjectId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setSubjectName(data.name || '');
            }
        }
        fetchSingleSubject();
    }, [subjectId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    
        if (subjectId) {
            const response = await updateSubject(subjectId, subjectName);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Subject Updated Successfully!");
            router.push('/Components/AllSubjects');
        } else {
            const response = await createSubject(subjectName);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Subject Created Successfully!");
            router.push('/Components/AllSubjects');
        }
    };   

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllSubjects')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{subjectId ? "Update Subject" : "Create Subject"}</h2>

            {/* Row 2 Content (textarea) */}
            <div className="mb-4">
                <label htmlFor="content" className='block mb-1 font-medium'>Subject Name</label>
                <input type="text" name="name" value={subjectName} onChange={(e) => setSubjectName(e.target.value)} placeholder="Maths" className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-400' />
            </div>
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {subjectId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default subjectForm