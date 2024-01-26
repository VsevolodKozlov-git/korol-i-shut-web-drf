import {createRouter, createWebHistory} from "vue-router"
import Visualization from "@/views/visualization"


const routes = [
    {
        path: '/visualization',
        component: Visualization
    }
]

const router = createRouter(({
    history: createWebHistory(), routes
}))

export default router;
