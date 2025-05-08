'use client'
import { createCat, createCatGrade, createExam, singleCat, singleCatGrade, singleExam, updateCat, updateCatGrade, updateExam } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const catGradeForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    const [catName, setCatName] = useState('');
    const [student, setStudent] = useState('');
    const [subject, setSubject] = useState('');
    const [marks, setMarks] = useState('');

    // get cat id from url
    const searchParams = useSearchParams();
    const catGradeId = searchParams.get('id');

    // fetch cat grade id
    useEffect(() => {
        const fetchSingleCatGrade = async () => {
            if (catGradeId ){
                const data = await singleCatGrade(catGradeId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setCatName(data.cat_name || '');
                setStudent(data.student || '');
                setSubject(data.subject || '');
                setMarks(data.marks || '');
            }
        }
        fetchSingleCatGrade();
    }, [catGradeId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
    
        if (catGradeId) {
            const response = await updateCatGrade(catGradeId, catName, student, subject, marks);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("CatGrading Updated Successfully!");
            router.push('/Components/AllCatGrades');
        } else {
            const response = await createCatGrade(catName, student, subject, marks);
            if (response.error) {
                setError(response.error);
                return;
            }
            alert("CatGrading Created Successfully!");
            router.push('/Components/AllCatGrades');
        }
    };    

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllCatGrades')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{catGradeId ? "Update Cat Grade" : "Create Cat Grade"}</h2>
            {/* Row 1: Exam name and subject */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div className="">
                    <label htmlFor="cat_name" className='block mb-1 font-medium'>Cat Code</label>
                    <input type="text" name="cat_name" value={catName} onChange={(e) => setCatName(e.target.value)} placeholder="C-001" className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-400' />
                </div>
                <div>
                <label htmlFor="duration" className='block mb-1 font-medium'>Student Code</label>
                <input
                    type="text"
                    id="student_code"
                    name="student_code"
                    value={student}
                    onChange={(e) => setStudent(e.target.value)}
                    placeholder="S-001"
                    className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-300'
                />
                </div>
            </div>

            {/* Row 4:  */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
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
                <div>
                    <label htmlFor="date_done" className='block mb-1 font-medium'>Marks</label>
                    <input type="number" id="cat_marks" name="cat_marks" value={marks} onChange={(e) => setMarks(e.target.value)}
                    className='w-full border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-yellow-300' />
                </div>
            </div>
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {catGradeId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default catGradeForm