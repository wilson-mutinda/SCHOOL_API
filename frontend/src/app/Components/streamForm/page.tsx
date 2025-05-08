'use client'
import { createClass, createExam, createStream, createSubject, singleClass, singleExam, singleStream, singleSubject, updateClass, updateExam, updateStream, updateSubject } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'

const streamForm = () => {
    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);
    const [fieldErrors, setFieldErrors] = useState<{[key: string]: string}>({});

    const [className, setClassName] = useState('');
    const [streamName, setStreamName] = useState('');

    // get class id from url
    const searchParams = useSearchParams();
    const streamId = searchParams.get('id');

    // fetch class id
    useEffect(() => {
        const fetchSingleStream = async () => {
            if (streamId ){
                const data = await singleStream(streamId);
                if (data.error) {
                    setError(data.error);
                    return;
                }
                setClassName(data.class_name || '');
                setStreamName(data.name || '');
            }
        }
        fetchSingleStream();
    }, [streamId]);

    // const handleSubmission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setFieldErrors({}); // clear previous errors
  
      const response = await (streamId
          ? updateStream(streamId, className, streamName)
          : createStream(className, streamName)
      );
  
      if (response.error || response.name || response.class_name) {
          const errors: { [key: string]: string } = {};
  
          // Catch known fields
          if (response.name) {
              errors['name'] = response.name;
          }
          if (response.class_name) {
              errors['class_name'] = response.class_name;
          }
  
          // Catch general error if it exists
          if (typeof response.error === 'string') {
              errors['form'] = response.error;
          }
  
          setFieldErrors(errors);
          return;
      }
  
      alert(`Stream ${streamId ? "Updated" : "Created"} Successfully!`);
      router.push('/Components/AllStreams');
  };
     

    // handle close
    const handleClose = () => {
        setClose(true);
        router.push('/Components/AllStreams')
    }

  return (
    <div className='bg-white-400 rounded-md max-w-4xl mx-auto p-6 shadow-2xl mt-10 relative'>
        {error && <p className='text-red-500 text-sm'>{error}</p>}
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <form onSubmit={handleSubmit} method="post">
            <h2 className='text-center font-bold text-gray-700 text-2xl mb-6'>{streamId ? "Update Stream" : "Create Stream"}</h2>

            {/* Row 3:Class and Stream */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                {/* Class field */}
                <div>
                    <label htmlFor="exam_class" className='block mb-1 font-medium'>Class</label>
                    <select
                        name="exam_class"
                        id="exam_class"
                        value={className}
                        onChange={(e) => setClassName(e.target.value)}
                        className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'
                    >
                        <option>Select Class</option>
                        <option value="F1">F1</option>
                        <option value="F2">F2</option>
                        <option value="F3">F3</option>
                        <option value="F4">F4</option>
                    </select>
                    {fieldErrors.class_name && <p className="text-red-500 text-sm">{fieldErrors.class_name}</p>}
                </div>

                {/* Stream field */}
                <div>
                    <label htmlFor="exam_stream" className='block mb-1 font-medium'>Stream</label>
                    <select
                        name="exam_stream"
                        id="exam_stream"
                        value={streamName}
                        onChange={(e) => setStreamName(e.target.value)}
                        className='w-full border border-gray-300 rounded-md p-2 bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300'
                    >
                        <option>Select Stream</option>
                        <option value="w">W</option>
                        <option value="e">E</option>
                    </select>
                    {fieldErrors.name && <p className="text-red-500 text-sm">{fieldErrors.name}</p>}
                </div>
            </div>

            {/* submit */}
            <div className="text-center pt-4">
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
                >
                    {streamId ? "Update" : "Create"}
                </button>
            </div>
        </form>
    </div>
  )
}

export default streamForm