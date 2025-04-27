'use client'
import { createRole, singleRole, updateRole } from '@/config/utils';
import Image from 'next/image'
import { useRouter, useSearchParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'
import { serialize } from 'v8';


const RoleForm = () => {

    const [close, setClose] = useState(false);
    const router = useRouter();
    const [error, setError] = useState<string | null>(null)

    const [name, setName] = useState('')

    // function to handle close
    const handleClose = async () => {
        setClose(true);
        router.push('/Components/AllRoles')
    }

    // fetch role id from the url
    const searchParams = useSearchParams();
    const roleId = searchParams.get('id');

    // fetch singlr role
    useEffect(() => {
        if (roleId) {
            const roleInfo = async () => {
                const data = await singleRole(roleId);
                setName(data.name)
            }
            roleInfo();
        }
    }, [roleId]);

    // handle submit
    const handleSubmit = async () => {
        const token = localStorage.getItem('access_token')
        if (!token) {
            alert("Login Required!");
            return;
        }

        if (roleId) {
            // handle update
            const request = await updateRole(roleId, name)
            if (request.error) {
                setError(request.error)
                return;
            }
            setError(null)
            alert("Role Updated Successfully!");
            router.push('/Components/AllRoles')
        } else {
            const request = await createRole(name);
            if (request.error) {
                setError(request.error);
                return;
            }
            setError(null)
            alert("Role Created Successfully")
            router.push('/Components/AllRoles')
        }
    }

  return (
    <div className='max-w-4xl mx-auto p-6 bg-white shadow-2xl rounded-2xl mt-10 relative'>
        <button onClick={handleClose} className='absolute right-3 top-2 rounded-full bg-red-500 p-2'>
            <Image src='/close.png' alt='' width={20} height={20} />
        </button>
        <h2 className="text-2xl font-semibold mb-6 text-center">{roleId ? "Update Role" : "Create Role"}</h2>
        <form action="" method="post">
            <div className="">
                <label htmlFor="name" className='font-semibold'>Name</label>
                <input required type="text" name="name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" className='mt-1 block w-full border border-gray-300 rounded-md p-2 focus:ring-blue-500 focus:border-blue-500'/>
            </div>
            {/* submit */}
            <div className="text-center pt-4">
            <button
                type="submit"
                className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700 transition"
            >
                {roleId ? "Update" : "Create"}
            </button>
            </div>
        </form>
    </div>
  )
}

export default RoleForm