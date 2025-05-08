'use client'
import { createClass, createExam, createSubject, singleClass, singleExam, singleSubject, updateClass, updateExam, updateSubject } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const classForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    const [className, setClassName] = useState('');

    // get class id from url
    const searchParams = useSearchParams();
    const classId = searchParams.get('id');

    // fetch class id
    useEffect(() => {
        const fetchSingleClass = async () => {
            if (classId ){
                const data = await singleClass(classId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setClassName(data.name || '');
            }
        }
        fetchSingleClass();
    }, [classId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    
        if (classId) {
            const response = await updateClass(classId, className);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Class Updated Successfully!");
            router.push('/Components/AllClasses');
        } else {
            const response = await createClass(className);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Class Created Successfully!");
            router.push('/Components/AllClasses');
        }
    };   

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllClasses')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{classId ? "Update Class" : "Create Class"}</h2>

            {/* Row 2 Content (textarea) */}
            <div className="mb-4">
                <label htmlFor="content" className='block mb-1 font-medium'>Class Name</label>
                <input type="text" name="name" value={className} onChange={(e) => setClassName(e.target.value)} placeholder="F1" className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-400' />
            </div>
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {classId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default classForm