<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;



class ApiConsume extends Controller
{

    public function test()
    {
       // $response = Http::get('http://example.com');
        //$response = Http::accept('application/json')->get('https://dummy.restapiexample.com/api/v1/employees');
        //$response = Http::get('https://dummy.restapiexample.com/api/v1/employees');
        //$response = Http::get('https://reqres.in/api/users');
       // $response = Http::post('https://reqres.in/api/users',['name' => "Gui","job" => "leader"]);
        // $response = Http::put('https://reqres.in/api/users/2',["name" => "sydney@fife","job" => "zoion"
        // ]);

       // $response = Http::accept('application/json')->get('https://shud.com.br/api/search-school');
        $response = Http::get('https://shud.com.br/api/search-school');

        //$response = Http::get('https://dummy.restapiexample.com/api/v1/employee/1');
        // $response = Http::put('https://dummy.restapiexample.com/api/v1/update/1',[
        //     "id" => 1,
        //     "employee_name" => "Tiger Nixon",
        //     "employee_salary" => 69,
        //     "employee_age" => 25,
        //     "profile_image" => "",
        // ]);

        // $response = Http::post('https://dummy.restapiexample.com/api/v1/create',[
        //     "name" => 'gui',
        //     "salary" => '10',
        //     "age" => '26',
        //     "id" => 22,
        // ]);
        //$response->data->id;
        //$response = Http::get('https://dummy.restapiexample.com/api/v1/employee/1',["employee_name" => "Tiger Nixonx"]);

        dd($response);

        $colle = $response->collect();

        dd($colle);

        //dd($colle["data"][0]["email"]);
        dd($response->json());



    }

}
