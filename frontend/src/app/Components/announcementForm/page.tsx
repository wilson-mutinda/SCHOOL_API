'use client'
import { createAnnouncement } from '@/config/utils';
import { timeLog } from 'console';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react'

const announcementForm = () => {

    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null)

    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');

    const [targetTeachers, setTargetTeachers] = useState(false);
    const [targetStudents, setTargetStudents] = useState(false);
    const [targetParents, setTargetParents] = useState(false);
    const [targetAdmins, setTargetAdmins] = useState(false)

    // handle create announcement
    const handleSubmit = async (e:React.FormEvent) => {
        e.preventDefault();

        const response = await createAnnouncement(
            title,
            description,
            targetTeachers,
            targetStudents,
            targetParents,
            targetAdmins
        );
        if (response.error) {
            setError(response.error);
            return;
        }
        alert("Announcement Created Successfully!")
        router.push('/Components/Dashboard')
    }

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/Dashboard')
    }
    
  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-600 text-2xl'>Create Announcement</h2>
            <div className="grid grid-cols-2">
                <div className="">
                    <label htmlFor="title" className='font-semibold'>Title</label>
                    <input type="text" name="title" value={title} onChange={(e) => setTitle(e.target.value)} required className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500'/>
                </div>
                <div className="mb-4 ml-2">
                    <label className='font-semibold block mb-2'>Target</label>
                    
                    <label className="inline-flex items-center mr-4">
                        <input type="checkbox" checked={targetTeachers} onChange={(e) => setTargetTeachers(e.target.checked)} name="target_teachers" />
                        <span className="ml-2">Teachers</span>
                    </label>
                    
                    <label className="inline-flex items-center mr-4">
                        <input type="checkbox" checked={targetStudents} onChange={(e) => setTargetStudents(e.target.checked)} name="target_students" />
                        <span className="ml-2">Students</span>
                    </label>
                    
                    <label className="inline-flex items-center mr-4">
                        <input type="checkbox" checked={targetAdmins} onChange={(e) => setTargetAdmins(e.target.checked)} name="target_admins" />
                        <span className="ml-2">Admins</span>
                    </label>

                    <label className="inline-flex items-center">
                        <input type="checkbox" checked={targetParents} onChange={(e) => setTargetParents(e.target.checked)} name="target_parents" />
                        <span className="ml-2">Parents</span>
                    </label>
                    </div>
            </div>
            <div className="grid grid-cols-1">
                <div className="">
                    <label htmlFor="content" className='font-semibold'>Content</label>
                    <input type="text" name="" value={description} onChange={(e) => setDescription(e.target.value)} required className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500' />
                </div>
            </div>
                {error && <p className='text-red-500 text-sm mt-2'>{error}</p>}
            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    Announce
                </button>
            </div>
        </form>
    </div>
  )
}

export default announcementForm