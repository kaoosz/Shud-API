<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\CandidateResourceController;
use App\Http\Controllers\Api\TopVotosBairro;
use App\Http\Controllers\Api\TopVotosCidade;
use App\Http\Controllers\Api\TopVotosEscola;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Response;
use Illuminate\Support\Facades\Route;




/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/


// Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
//     return $request->user();
// });


Route::get('csvtestone',function(){

    #shell_exec("python3 /home/guilherme/Development/Shud-API/example-app/resources/filepython/Geracsv/Gerador.py");
    //exec("python3 /home/guilherme/Development/Shud-API/example-app/resources/filepython/Geracsv/Gerador.py");
    //$two = '"http://localhost:8000/api/candidatos/candidatos?ANO=2018&NR_CANDIDATO=3133&csv=csv&urna=MARCELO%20ARO"';

    //$two = "http://142.93.244.160/api/candidatos/candidatos?bairro=bairro2018&ANO=2018&urna=MARCELO%20ARO&NR_CANDIDATO=3133";
    $two = "http://142.93.244.160/api/candidatos/candidatos?bairro=bairro2018&ANO=2018&urna=LENINHA&NR_CANDIDATO=13456";
    
    
    $fu = shell_exec("python3 /home/guilherme/Development/Shud-API/example-app/public/Gerador.py {$two}");

    var_dump($fu);
    
    //funciona
    // $file = public_path()."/mine.csv";
    // $headers = array(
    //     'Content-Type: application/pdf',
    // );
    // return Response::download($file, 'mine.csv', $headers);
});

Route::get('candidatosMaisVotadosCidade',[TopVotosCidade::class,'CidadeMaisVotada']);//->only('show','index');
Route::get('candidatosMaisVotadosEscola',[TopVotosEscola::class,'EscolaMaisVotada']);//->only('show','index');
Route::get('candidatosMaisVotadosBairro',[TopVotosBairro::class,'BairroMaisVotada']);//->only('show','index');


Route::post('login',[AuthController::class,'login']);
Route::post('/password/email',[AuthController::class,'sendPasswordResetLinkEmail']);
Route::post('/password/reset',[AuthController::class,'resetPassword']);

Route::apiResource('candidatos',CandidateResourceController::class)->only('show','index');



Route::group(['middleware' => ['auth:sanctum']],function(){

    //Route::apiResource('candidatos',CandidateResourceController::class)->only('show','index');
});

Route::get('creat',function(){

    User::create([
        'name' => 'allan',
        'email' => 'allan@gmail.com',
        'password' => Hash::make('123'),
        'is_admin' => true,
    ]);
});