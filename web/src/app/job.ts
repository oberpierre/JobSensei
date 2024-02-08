export interface Job {
    uuid: string;
    title: string;
    summary?: string;
    url?: string;
    skills?: string[];
    locations?: {
        city?: string;
        country?: string;
    }[];
    responsibilities?: string[];
    qualifications?: {
        required?: string[];
        preferred?: string[];
    };
    createdOn?: string;
    isRecent?: boolean;
    deletedOn?: string;
}
