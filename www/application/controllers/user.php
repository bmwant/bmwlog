<?php

class User extends CI_Controller {

    public function __construct() {
        parent::__construct();
        $this->load->model('user_model');
        //$this->load->model('tag_model');
    }

    public function index() {
        $data['user'] = $this->user_model->get_post();
        $data['title'] = 'All users list';
        $this->load->view('templates/header', $data);
        $this->load->view('user/index', $data);
        $this->load->view('templates/footer');
    }

    public function view($id) {

        $data['item'] = $this->post_model->get_user($id);

        if (empty($data['item'])) {
            show_404();
        }

        //$data['title'] = $data['item']['title'];

        $this->load->view('templates/header', $data);
        $this->load->view('user/view', $data);
        $this->load->view('templates/footer');
    }

    public function add() {
        $this->load->helper('form');
        $this->load->library('form_validation');
        $this->load->helper('url');
        
        $data['title'] = 'Add new post';

        $this->form_validation->set_rules('title', 'title', 'required');
        $this->form_validation->set_rules('text', 'text', 'required');

        if ($this->form_validation->run() === FALSE) {
            $this->load->view('templates/header', $data);
            $this->load->view('user/add');
            $this->load->view('templates/footer');
        } else {
            $this->post_model->add_user();
            redirect('user/view');
        }
    }

}
