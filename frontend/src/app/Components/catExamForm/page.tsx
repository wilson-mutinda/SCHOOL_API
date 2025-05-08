'use client'
import { createCat, createCatAndExam, createCatGrade, createExam, singleCat, singleCatAndExamGrade, singleCatGrade, singleExam, updateCat, updateCatAndExam, updateCatGrade, updateExam } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const catExamForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    const [className, setClassName] = useState('');
    const [streamName, setStreamName] = useState('');
    const [classStudent, setClassStudent] = useState('');
    const [subject, setSubject] = useState('');

    // get catandexam id from url
    const searchParams = useSearchParams();
    const catExamId = searchParams.get('id');

    // fetch cat and exam id
    useEffect(() => {
        const fetchSingleCatAndExam = async () => {
            if (catExamId ){
                const data = await singleCatAndExamGrade(catExamId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setClassName(data.class_name || '');
                setStreamName(data.stream_name || '');
                setClassStudent(data.class_student || '');
                setSubject(data.subject || '');
            }
        }
        fetchSingleCatAndExam();
    }, [catExamId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    
        if (catExamId) {
            const response = await updateCatAndExam(catExamId, className, streamName, classStudent, subject);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("CatExam Updated Successfully!");
            router.push('/Components/AllCatsAndExams');
        } else {
            const response = await createCatAndExam(className, streamName, classStudent, subject);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("CatAndExam Created Successfully!");
            router.push('/Components/AllCatsAndExams');
        }
    };    

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllCatsAndExams')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{catExamId ? "Update CatAndExam" : "Create CatAndExam"}</h2>
            {/* Row 1: Exam name and subject */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div>
                <label htmlFor="duration" className='block mb-1 font-medium'>Student Code</label>
                <input
                    type="text"
                    id="student_code"
                    name="student_code"
                    value={classStudent}
                    onChange={(e) => setClassStudent(e.target.value)}
                    placeholder="S-001"
                    className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-300'
                />
                </div>
                <div className="">
                    <label htmlFor="subject" className='block mb-1 font-medium'>Class</label>
                    <select name="subject" id="subject" value={className} onChange={(e) => setClassName(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Class</option>
                        <option value="f1">F1</option>
                        <option value="f2">F2</option>
                        <option value="f3">F3</option>
                        <option value="f4">f4</option>
                    </select>
                </div>
            </div>

            {/* Row 4:  */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div className="">
                    <label htmlFor="subject" className='block mb-1 font-medium'>Class</label>
                    <select name="subject" id="subject" value={streamName} onChange={(e) => setStreamName(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Stream</option>
                        <option value="w">W</option>
                        <option value="e">E</option>
                    </select>
                </div>
            <div className="">
                    <label htmlFor="subject" className='block mb-1 font-medium'>Subject</label>
                    <select name="subject" id="subject" value={subject} onChange={(e) => setSubject(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Subject</option>
                        <option value="English">English</option>
                        <option value="Kiswahili">Kiswahili</option>
                        <option value="Maths">Maths</option>
                        <option value="Chemistry">Chemistry</option>
                        <option value="Physics">Physics</option>
                        <option value="Biology">Biology</option>
                        <option value="Geography">Geography</option>
                        <option value="Cre">Cre</option>
                        <option value="History">History</option>
                        <option value="Agriculture">Agriculture</option>
                        <option value="Business-Studies">Business-Studies</option>
                        <option value="Computer-Studies">Computer-Studies</option>
                    </select>
                </div>
            </div>
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {catExamId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default catExamForm