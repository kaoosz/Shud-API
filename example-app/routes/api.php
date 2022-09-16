<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\CandidateResourceController;
use App\Http\Controllers\Api\Candidates;
use App\Http\Controllers\Api\CandidatosController;
use App\Http\Controllers\Api\Testing;
use App\Http\Controllers\Api\TopVotos;
use App\Http\Controllers\Api\TopVotosBairro;
use App\Http\Controllers\Api\TopVotosCidade;
use App\Http\Controllers\Api\TopVotosEscola;
use App\Http\Controllers\Api\VotesNeighborhoods as ApiVotesNeighborhoods;
use App\Http\Resources\CandidateResource;
use App\Models\Candidate;
use App\Models\User;
use App\Models\VotesNeighborhoods;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Hash;
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


Route::get('candidatosMaisVotadosCidade',[TopVotosCidade::class,'CidadeMaisVotada']);//->only('show','index');
Route::get('candidatosMaisVotadosEscola',[TopVotosEscola::class,'EscolaMaisVotada']);//->only('show','index');
Route::get('candidatosMaisVotadosBairro',[TopVotosBairro::class,'BairroMaisVotada']);//->only('show','index');


Route::post('login',[AuthController::class,'login']);
Route::post('/password/email',[AuthController::class,'sendPasswordResetLinkEmail']);
Route::post('/password/reset',[AuthController::class,'resetPassword']);

Route::apiResource('candidatos',CandidateResourceController::class)->only('show','index');
Route::post('candidatosGera',[CandidateResourceController::class,'GeraPython']);


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
