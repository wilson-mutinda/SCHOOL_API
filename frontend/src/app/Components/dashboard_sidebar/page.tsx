import Image from 'next/image'
import Link from 'next/link'
import { it } from 'node:test'
import React from 'react'

// main components
const mainComponents = [
    {
        title: 'MAIN MENU',
        items: [
            {
                text: 'Dashboard',
                logo: '/dashboard.png',
                link: 'Dashboard'
            },
            {
                text: 'Teacher Portal',
                logo: '/teacher.png',
                link: '/'
            },
            {
                text: 'Parent Portal',
                logo: '/parent.png',
                link: '/'
            },
            {
                text: 'Student Portal',
                logo: '/student.png',
                link: '/'
            },
            {
                text: 'Admissions',
                logo: '/admission.png',
                link: '/'
            },
            {
                text: 'Reports',
                logo: '/report.png',
                link: '/'
            },
            {
                text: 'Conferencing',
                logo: '/meet.png',
                link: '/',
            },
            {
                text: 'About',
                logo: '/about.png',
                link: '/'
            },
        ]
    },
    {
        title: 'ACCOUNT',
        items: [
            {
                text: 'Logout',
                logo: '/logout.png',
                link: '/'
            }
        ]
    }
]

const DashboardSideBar = () => {
  return (
    <div>
        {/* Title Logo and main componetns */}
        <div className="">
            {/* Title Logo */}
            <div className="hover:bg-green-400 hover:text-white">
                <Link href='/' className=''>
                    <div className="flex items-center gap-3 p-3">
                        <Image src='/logo.png' alt='' width={20} height={20} className='w-10 h-10'/>
                        <span className='font-semibold'>Bidii School</span>
                    </div>
                </Link>
            </div>
            {/* main components */}
            <div className="p-2">
                {mainComponents.map((section, sectionIndex)=> (
                    <div className="" key={sectionIndex}>
                        <h3 className='font-semibold text-[#808080] p-2 mt-2'>{section.title}</h3>
                        {section.items.map((item, itemIndex) => (
                            <Link href={item.link} key={itemIndex}>
                                <div className="flex items-center gap-3 p-3 font-semibold hover:bg-[#708090] rounded-md hover:text-white">
                                    <Image src={item.logo} alt='' width={20} height={20} className='w-8 h-8 p-1 bg-white rounded-md items-center'/>
                                    <span className='hidden md:block'>{item.text}</span>
                                </div>
                            </Link>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    </div>
  )
}

export default DashboardSideBar