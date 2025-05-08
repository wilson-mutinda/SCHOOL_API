'use client'
import { createCat, createExam, singleCat, singleExam, updateCat, updateExam } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const catForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    const [catName, setCatName] = useState('');
    const [content, setContent] = useState('');
    const [catClass, setCatClass] = useState('');
    const [catStream, setCatStream] = useState('');
    const [subject, setSubject] = useState('');
    const [duration, setDuration] = useState('');
    const [dateDone, setDateDone] = useState('');
    const [startTime, setStartTime] = useState('');
    const [catTerm, setCatTerm] = useState('');

    // get cat id from url
    const searchParams = useSearchParams();
    const catId = searchParams.get('id');

    // fetch exam id
    useEffect(() => {
        const fetchSingleCat = async () => {
            if (catId ){
                const data = await singleCat(catId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setCatName(data.cat_name || '');
                setSubject(data.subject || '');
                setContent(data.content || '');
                setCatClass(data.cat_class || '');
                setCatStream(data.cat_stream || '');
                setDuration(data.duration || '');
                setDateDone(data.date_done || '');
                setStartTime(data.start_time || '');
                setCatTerm(data.cat_term || '');
            }
        }
        fetchSingleCat();
    }, [catId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    
        if (catId) {
            const response = await updateCat(catId, catName, content, catClass, catStream, subject, duration, dateDone, startTime, catTerm);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Cat Updated Successfully!");
            router.push('/Components/AllCats');
        } else {
            const response = await createCat(catName, content, catClass, catStream, subject, duration, dateDone, startTime, catTerm);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("Cat Created Successfully!");
            router.push('/Components/AllCats');
        }
    };    

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllCats')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{catId ? "Update Cat" : "Create Cat"}</h2>
            {/* Row 1: Exam name and subject */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div className="">
                    <label htmlFor="exam_name" className='block mb-1 font-medium'>Cat Name</label>
                    <input type="text" name="exam_name" value={catName} onChange={(e) => setCatName(e.target.value)} placeholder="End Term Exam" className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-400' />
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

            {/* Row 2 Content (textarea) */}
            <div className="mb-4">
                <label htmlFor="content" className='block mb-1 font-medium'>Cat Content</label>
                <textarea name="content" value={content} onChange={(e) => setContent(e.target.value)} placeholder='1. Define what is a Vowel.. 2. Define..' className='w-full border border-gray-300 rounded-md p-2 resize-none focus:outline-none focus:ring-2 focus:ring-yellow-300'></textarea>
            </div>

            {/* Row 3:Class and Stream */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div className="">
                    <label htmlFor="exam_class" className='block mb-1 font-medium'>Class</label>
                    <select name="exam_class" id="exam_class" value={catClass} onChange={(e) => setCatClass(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Class</option>
                        <option value="F1">F1</option>
                        <option value="F2">F2</option>
                        <option value="F3">F3</option>
                        <option value="F4">F4</option>
                    </select>
                </div>

                <div className="">
                    <label htmlFor="exam_stream" className='block mb-1 font-medium'>Stream</label>
                    <select name="exam_stream" id="exam_stream" value={catStream} onChange={(e) => setCatStream(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Stream</option>
                        <option value="w">W</option>
                        <option value="e">E</option>
                    </select>
                </div>
            </div>

            {/* Row 4: Duration & Date */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
                <label htmlFor="duration" className='block mb-1 font-medium'>Duration (HH:MM:SS)</label>
                <input
                    type="text"
                    id="duration"
                    name="duration"
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                    placeholder="00:40:00"
                    pattern="^([0-9]{2}):([0-5][0-9]):([0-5][0-9])$"
                    title="Duration must be in the format HH:MM:SS"
                    className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-300'
                />
                </div>

                <div>
                    <label htmlFor="date_done" className='block mb-1 font-medium'>Date</label>
                    <input type="date" id="date_done" name="date_done" value={dateDone} onChange={(e) => setDateDone(e.target.value)}
                    className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-300' />
                </div>
            </div>
            {/* Row 5: Start Time & Term */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                    <label htmlFor="start_time" className='block mb-1 font-medium'>Start Time</label>
                    <input type="time" id="start_time" name="start_time" value={startTime} onChange={(e) => setStartTime(e.target.value)}
                    className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-300' />
                </div>

                <div>
                    <label htmlFor="exam_term" className='block mb-1 font-medium'>Cat Term</label>
                    <select name="exam_term" id="exam_term" value={catTerm} onChange={(e) => setCatTerm(e.target.value)} className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'>
                        <option>Select Term</option>
                        <option value="term1">Term1</option>
                        <option value="term2">Term2</option>
                        <option value="term3">Term3</option>
                    </select>
                </div>
            </div>
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {catId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default catForm